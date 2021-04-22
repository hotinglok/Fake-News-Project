# This code was originally made by Vishwa (@v1shwa) and can be found at https://github.com/v1shwa/document-similarity.
# This code is used under the MIT License stated in the repository above.
# Minor edits have been made for the purposes of this project.

import numpy as np
from .rss_feeds import sources

class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc: str) -> np.ndarray:
        """
        Identify the vector values for each word in the given document
        :param doc:
        :return:
        """
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    # The original
    def calculate_similarity(self, source_doc, target_docs=None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                #print("Result {} is higher than threshold".format(doc))
                results.append({"score": sim_score, "doc": doc})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)

        print("Finished calculating")
        return results


    # Legacy used in main.py
    def calculateSimilarity(self, root_source, other_source, threshold=0):
        # Add in the entire dataframe, use iterrows() here instead of the for loop
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        source_vec = self.vectorize(root_source)
        results = []
        for index, row in other_source.iterrows():
            target_vec = self.vectorize(row['title'])
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                #print("Result {} is higher than threshold".format(doc))
                results.append({"score": sim_score, 
                                "title": row['title'],
                                "description": row['description'],
                                "link": row['link'],
                                "pubDate": row['pubDate'],
                                "category": row['category'],
                                "source": row['source']})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)
        print("Finished calculating")
        if len(results) == 0:
            print('There were no matching articles above the threshold')
        else:
            test = other_source.iloc[0]
            print('{}:'.format(test['source']))
            for result in results:
                print("Score:{}\nTitle:{}\nLink:{}\n".format(result.get('score'), result.get('title'), result.get('link')))
            print('-----END-----')    
        return results

    # This returns a dict in a similar structure to getData in the API
    def calcSim(self, root_source, other_sources, threshold=0):
        # Add in the entire dataframe, use iterrows() here instead of the for loop
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        # This will just be a string
        source_vec = self.vectorize(root_source)

        # Need an object to hold the results for each other source
        data = {}

        # Loop through each of the other sources
        for source in other_sources:
            results = []
            for index, row in source.get('data').iterrows():
                target_vec = self.vectorize(row['title'])
                sim_score = self._cosine_sim(source_vec, target_vec)
                if sim_score > threshold:
                    #print("Result {} is higher than threshold".format(doc))
                    results.append({"score": sim_score, 
                                    "title": row['title'],
                                    "description": row['description'],
                                    "link": row['link'],
                                    "pubDate": row['pubDate'],
                                    "category": row['category'],
                                    "source": row['source']})
                # Sort results by score in desc order
                results.sort(key=lambda k: k["score"], reverse=True)
            print("Finished calculating")
            if len(results) == 0:
                continue
            else:
                source_name = source.get('name').lower().replace(' ', '_')
                data['{}'.format(source_name)] = results

        return data

    def calculate_final(self, source_doc, target_docs=None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                #print("Result {} is higher than threshold".format(doc))
                results.append({"score": sim_score, "doc": doc})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)

        print("Finished calculating")
        return results