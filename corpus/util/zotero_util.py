import requests
import os



class ZoteroUtil:
    def __init__(self):
        pass

    def download_pdf(url, save_name):
        try:
            if not save_name.endswith(".pdf"):
                save_name += ".pdf"
            download_dir = 'zotero_pdfs'
            save_path = os.path.join(download_dir, save_name)

            encoded_url = url
            
            response = requests.get(encoded_url, stream=True)
            response.raise_for_status() 

            if 'application/pdf' not in response.headers.get('Content-Type', ''):
                raise ValueError(f"URL does not point to a PDF: {url}")
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("PDF Downloaded.")

            
        except Exception:
            print(f"PDF not found. Failed to download.")