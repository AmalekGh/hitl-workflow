import os
from langchain.schema.document import Document
from pdfminer.high_level import extract_text
from langchain.text_splitter import NLTKTextSplitter
import warnings
import re
import numpy as np

class DocumentUtil:
    def __init__(self):
        pass

    def split_text_by_paragraphs(text, source):
        paragraphs = text.split("\n\n\n")
        return [Document(page_content=para.strip(), metadata={"source": source}) for para in paragraphs if para.strip()]
    
    
    def load_documents_from_text(self, data_path):
        documents = []

        for file_name in os.listdir(data_path):
            if file_name.endswith("2403.07541v2.txt"):
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

    def get_text_without_references(self,path):
        text = extract_text(path)

        return self.remove_references(self, text)
    
    def text_splitter(self, path):
        warnings.filterwarnings('ignore')
        splitter = NLTKTextSplitter()
        chunks = splitter.split_text(self.get_text_without_references(self, path))
        full_sentences = []
        for i in chunks:
            sentences = i.split('\n\n')
            for j in sentences:
                full_sentences.append(j)

        seen = set()
        no_duplicates = []

        for item in full_sentences:
            if item not in seen:
                no_duplicates.append(item)
                seen.add(item)

        merged_sentences = []
        i = 0 
        j=0
        while i < len(no_duplicates):
            sentence = no_duplicates[i].strip()

            if sentence.endswith('e.g.') or sentence.endswith('al.') or sentence.endswith('al.'):
                if i+1 < len(sentences):
                    sentence += " " + no_duplicates[i+1].strip()
                    i+=1
            merged_sentences.append(sentence)
            i+=1

        while j < len(merged_sentences):
            merged_sentences[j] = merged_sentences[j].replace('-\n', '')
            merged_sentences[j] = merged_sentences[j].replace('\n',' ')
            j+=1

        return merged_sentences

    def combine_sentences(sentences, window_size=1):
        warnings.filterwarnings('ignore')
        for i in range(len(sentences)):
            combined_sentence=''

            for j in range(i - window_size, i):
                if j>=0:
                    combined_sentence+=sentences[j]['sentence']+' '
            combined_sentence+=sentences[i]['sentence']

            for j in range(i+1, i+1+window_size):
                if j < len(sentences):
                    combined_sentence+= ' ' + sentences[j]['sentence']
            sentences[i]['combined_Sentence']= combined_sentence
        return sentences
            


    