import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
    
    def calculate_cosine_distances(sentences):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i+1]['combined_sentence_embedding']

            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]

            distance = 1 - similarity
            distances.append(distance)

            sentences[i]['distance to next'] = distance

        return distances, sentences
    
    def get_split_indices(distances):

        breakpoint_percentile_threshold = 65
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)

        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]

        return indices_above_thresh

    def split_using_distances(split_distances, sentences_list):
        start_index = 0 

        chunks_final = []

        for index in split_distances:
            end_index = index - 1 

            group = sentences_list[start_index:end_index+1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks_final.append(combined_text)

            start_index = index

        if start_index < len(sentences_list):
            combined_text = ' '.join([d['sentence'] for d in sentences_list[start_index:]])
            chunks_final.append(combined_text)

        return chunks_final