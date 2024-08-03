import requests
import re
import os

# Regular expression to remove invalid characters from filenames
invalid_char_re = re.compile(r'[<>:"/\\|?*]')

class SemanticScholar:
    def __init__(self):
        pass

    def semanticscholar(self, query, limits):
        # Define the API endpoint URL
        url = 'https://api.semanticscholar.org/graph/v1/paper/search'

        # More specific query parameters
        query_params = {
            'query': query,
            'limit': limits,  # Number of papers to fetch
            'fields': 'paperId,title,openAccessPdf'
        }

        # Send the API request
        response = requests.get(url, params=query_params)

        # Check response status
        if response.status_code == 200:
            response_data = response.json()

            # Filter papers with open access PDF
            papers_with_pdf = [paper for paper in response_data.get('data', []) if paper.get('openAccessPdf')]

        else:
            print(f"Request to fetch paper failed with status code {response.status_code}: {response.text}")
            papers_with_pdf = []

        return papers_with_pdf

    def sanitize_filename(self, filename):
        """Sanitize the filename by replacing invalid characters."""
        return invalid_char_re.sub('_', filename)

    def download_pdfs(self, query, limit=50):
                
        print("Querying Semantic Scholar...")
        papers_with_pdf = self.semanticscholar(query, limit)
        os.makedirs('pdfs_corpus', exist_ok=True)

        print(f"Number of papers with PDF: {len(papers_with_pdf)}")

        headers = {
            'Accept': 'application/pdf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for paper in papers_with_pdf:
            open_access_pdf = paper.get('openAccessPdf', {})
            title = paper.get('title', {})

            pdf_url = open_access_pdf.get('url')

            if pdf_url:
                save_name = self.sanitize_filename(title)

                pdf_response = requests.get(pdf_url, headers=headers, allow_redirects=True)
                if pdf_response.status_code == 200:
                    pdf_path = os.path.join('pdfs_corpus', f'{save_name}.pdf')

                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                else:
                    print(f"Failed to download PDF for paper titled: {title}")

        print("Semantic Scholar was successfully queried...")
