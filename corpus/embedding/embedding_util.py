import ollama
from vectordb import Memory
import faiss
import numpy as np

class EmbeddingUtil:
    def __init__(self):
        pass

    def ollama_embed_document(self, documents, model="nomic-embed-text"):
        embeddings = []
        for d in documents:
            response = ollama.embeddings(model, prompt=d)
            embeddings.append(response["embedding"])
        return embeddings

    def ollama_embed_query(self, query, model="nomic-embed-text"):
        return ollama.embeddings(model, prompt=query)["embedding"]

    def compute_top_k_ollama(self, documents, query):
        embedded_documents = self.ollama_embed_document(self, documents, model="nomic-embed-text")
        query_embedding = self.ollama_embed_query(self, query, model="nomic-embed-text")

        embeddings_np = np.array(embedded_documents).astype('float32')
        faiss.normalize_L2(embeddings_np)
        dimension = embeddings_np.shape[1]
        index = faiss.IndexFlatIP(dimension)

        index.add(embeddings_np)

        query_np = np.array([query_embedding]).astype('float32')

        faiss.normalize_L2(query_np)

        k=10
        distances, indicies = index.search(query_np, k)

        result = ""
        for i in range(k):
            result += f"{documents[indicies[0][i]]}\n"

        return result
        

    
    def vectordb_embedding_search(self, chunked_documents, query):
        memory = Memory()

        metadata = {"Test_metadata"}
        
        memory.save(chunked_documents, metadata)

        results = memory.search(query, top_n=10)

        return results
    

