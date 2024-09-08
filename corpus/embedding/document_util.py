import os
from langchain.schema.document import Document
import re
import numpy as np
import spacy


class DocumentUtil:
    def __init__(self):
        pass

    def split_text_by_paragraphs(text, source):
        paragraphs = text.split("\n\n\n")
        return [Document(page_content=para.strip(), metadata={"source": source}) for para in paragraphs if para.strip()]
    
    
    def load_documents_from_text(self, data_path):
        documents = []

        for file_name in os.listdir(data_path):
            if file_name.endswith("F95SXDZF.txt"):
                file_path = os.path.join(data_path, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    documents.append(Document(page_content=text, metadata={"source": file_path}))
        return documents
    
    def remove_references(self, text):

        reference_headings = [
            r'^\s*References\s*$',
            r'^\s*Bibliography\s*$',
            r'^\s*Reference\s*$',
            r'^\s*REFERENCES\s*$',
            r'^\s*BIBLIOGRAPHY\s*$',
            r'^\s*REFERENCE\s*$'
        ]

        pattern = re.compile('|'.join(reference_headings), re.IGNORECASE)

        lines = text.split('\n')

        for i, line in enumerate(lines):
            if pattern.match(line.strip()):
                return '\n'.join(lines[:i])
        return text
    
    def get_text_from_document(self, path):
        document = self.load_documents_from_text(self, path)
        text = self.remove_references(self, document[0].page_content)
        return text




    