import numpy as np
import spacy


class ChunksUtil:
    def __init__(self):
        pass

    def process(text):
        nlp = spacy.load('en_core_web_sm')
        document = nlp(text)
        sentences = list(document.sents)
        vectors = np.stack([sent.vector / sent.vector_norm for sent in sentences])
        return sentences, vectors
    
    def cluster_text(senteces, vectors, threshold):
        clusters = [[0]]
        for i in range(1, len(senteces)):
            if np.dot(vectors[i], vectors[i-1]) < threshold:
                clusters.append([])
            clusters[-1].append(i)
        return clusters
    
    def compute_chunks(self, text, threshold=0.3):
        clusters_len = []
        final_chunks = []

        sentences, vectors = self.process(text)

        clusters = self.cluster_text(sentences, vectors, threshold)

        for cluster in clusters:
            cluster_txt = ' '.join([sentences[i].text for i in cluster])
            cluster_len = len(cluster_txt)


            if cluster_len < 60:
                    continue
            elif cluster_len > 3000:
                threshold = 0.6
                sents_div, vecs_div = self.process(cluster_txt)
                reclusters = self.cluster_text(sents_div, vecs_div, threshold)
                
                for subcluster in reclusters:
                    div_txt = ' '.join([sents_div[i].text for i in subcluster])
                    div_len = len(div_txt)
                        
                    if div_len < 60 or div_len > 3000:
                        continue
                        
                    clusters_len.append(div_len)
                    final_chunks.append(div_txt)
                        
            else: 
                clusters_len.append(cluster_len)
                final_chunks.append(cluster_txt)

        return final_chunks