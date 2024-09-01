from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import os


class PdfUtil:

    def __init__(self):
        pass

    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        print("PDF to text conversion completed!")
        return text

    def save_text(file_path, text):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        

    def remove_standalone_numbers(text):
        number_pattern = r"^\s*\d+\s*$"

        lines = text.splitlines()

        filtered_lines = [line for line in lines if not re.match(number_pattern, line)]

        cleaned_text = "\n".join(filtered_lines)

        return cleaned_text
    
    def convert_pdfs_in_folder(self, folder_path, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                text = self.convert_pdf_to_txt(pdf_path)
                text = self.remove_standalone_numbers(text)

                # Save the text with the same name as the PDF but with a .txt extension
                txt_filename = f"{os.path.splitext(filename)[0]}.txt"
                txt_path = os.path.join(output_folder, txt_filename)
                self.save_text(txt_path, text)
                print(f"Converted and saved {filename} to {txt_filename}")

