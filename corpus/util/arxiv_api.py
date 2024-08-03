import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
import re
from urllib.parse import quote


invalid_char_re = re.compile(r'[<>:"/\\|?*]')


class Arxiv(object):
    def __init__(self):
        pass

    def arxiv_payload(self, keyword, size, start=0):

        headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://arxiv.org/search/?query=Multi-label+text+classification&searchtype=all&abstracts=show&order=&size=100&start=200",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

        params = (
            ("searchtype", "all"),
            ("query", keyword.lower()),
            ("abstracts", "show"),
            ("size", str(size)),
            ("order", ""),
            ("start", str(start)),
        )
        response = requests.get(
            "https://arxiv.org/search/", headers=headers, params=params
        )
        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def arxiv_html_fetch(self, soup):

        final_result = []
        final_out = soup.find_all("li", {"class": "arxiv-result"})

        for paper in final_out:

            temp_result = {}
            title = paper.find("p", {"class": "title is-5 mathjax"}).text.strip()
            paper_link = paper.find("p", {"class": "list-title is-inline-block"}).find(
                "a", href=True
            )["href"]
            pdf_link = paper.find("a", string="pdf", href=True)["href"]
            
            temp_result["title"] = title
            temp_result["link"] = paper_link
            temp_result["pdf_link"] = pdf_link
            final_result.append(temp_result)
        df = pd.DataFrame(final_result)
        return df

    def arxiv(self, keyword, limit, max_pages=10, api_wait=10):

        all_pages = []
        for page in tqdm(range(max_pages)):
            arxiv_pay_load = self.arxiv_payload(keyword, limit, start=page)
            arxiv_soup = self.arxiv_html_fetch(arxiv_pay_load)
            all_pages.append(arxiv_soup)
            time.sleep(api_wait)

        df = pd.concat(all_pages)
        return df.reset_index(drop=True)




    invalid_char_re = re.compile(r'[<>:"/\\|?*]')


    def sanitize_filename(self, filename):

        return invalid_char_re.sub('_', filename)

    def download_pdf(self, query, limit=100):

        arxiv_results = self.arxiv(query, limit)

        download_dir = "pdfs_corpus"
        os.makedirs(download_dir, exist_ok=True)

        pdf_links = arxiv_results["pdf_link"]
        titles = arxiv_results["title"]  

        for url, save_name in zip(pdf_links, titles):

            try:
                if not save_name.endswith(".pdf"):
                    save_name += ".pdf"

                save_name = self.sanitize_filename(save_name)
                
                save_path = os.path.join(download_dir, save_name)

                encoded_url = quote(url, safe=":/")
                
                response = requests.get(encoded_url, stream=True)
                response.raise_for_status() 

                if 'application/pdf' not in response.headers.get('Content-Type', ''):
                    raise ValueError(f"URL does not point to a PDF: {url}")
                
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
            except Exception as e:
                print(f"Failed to download {url}: {e}")
