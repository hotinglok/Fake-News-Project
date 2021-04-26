# This code was originally made by Vishwa (@v1shwa) and can be found at https://github.com/v1shwa/document-similarity.
# This code is used under the MIT License stated in the repository above.
# Edits have been made for the purposes of this project.

from .rss_feeds import sources
import numpy as np
import re
import string

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
        words = []
        # Regex added since punctuation gets in the way
        regex = re.compile('[^a-zA-Z]') # Only latin alphabetical characters

        # doc.translate to remove all punctuation (though it doesn't catch punctuation pre/suffixed to words)
        for word in doc.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).split(" "):
            word = regex.sub('', word)    # Gets rid of what the above can't catch
            if word not in self.stopwords:
                if word != '':
                    words.append(word)

        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                print(word)
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it. -@hotinglok comment: I don't know if there is for general use cases.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    # This returns a dict in a similar structure to getData in the API
    def collateArticles(self, root_source, other_sources, threshold=0):
        # Add in the entire dataframe, use iterrows() here instead of the for loop
        """Calculates & returns similarity scores between given source document & all
        the target documents."""

        # This will just be a string
        source_vec = self.vectorize(root_source)

        # Need an object to hold the results for each other source
        data = {}

        # Loop through the array of other sources
        for source in other_sources:
            results = []
            for index, row in source.get('data').iterrows():
                target_vec = self.vectorize(row['title'])
                sim_score = self._cosine_sim(source_vec, target_vec)
                if sim_score > threshold:
                    #print("Result {} is higher than threshold".format(doc))
                    results.append({"score": float(sim_score), 
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


    def calculateSimilarity(self, data_type, root_list, other_list, threshold=0):

        first_source = {'sorted_{}'.format(data_type): []}
        second_source = {'sorted_{}'.format(data_type): []}
        swapped = False
        # Check which list is shorter. If the other list is shorter, swap the values
        if len(other_list) < len(root_list):
            temp = root_list
            root_list = other_list
            other_list = temp
            swapped = True

        # While root_list is not empty
        while root_list:
            # Ensure that the loop won't be reading null from other_list
            if len(other_list) == 0:
                break
            
            # Get the first sentence in root_list. Always true since the sentence is removed at the end of the for loop
            root_quote = root_list[0].get('sentence')
            source_vec = self.vectorize(root_quote)

            # Temporary results list
            results = []

            # For each sentence in other_list
            for item in other_list:
                target_vec = self.vectorize(item.get('sentence'))
                sim_score = self._cosine_sim(source_vec, target_vec)
                if sim_score > threshold:
                    results.append({"score": sim_score, "item": item})
                # Sort results by score in desc order
                results.sort(key=lambda k: k["score"], reverse=True)

            # Match the sentence with the highest similarity score
            result_sentence = results[0].get('item').get('sentence')
            result_index = results[0].get('item').get('position')

            # Remove matched pair from respective lists
            if swapped == True:
                first_source.get('sorted_{}'.format(data_type)).append({'sentence': result_sentence, 'index': result_index, 'score': results[0].get('score')})
                second_source.get('sorted_{}'.format(data_type)).append(root_list[0])
            else:
                first_source.get('sorted_{}'.format(data_type)).append(root_list[0])
                second_source.get('sorted_{}'.format(data_type)).append({'sentence': result_sentence, 'index': result_index, 'score': results[0].get('score')})

            # Secondary check to ensure that there won't be any out of bounds errors
            if len(other_list) > 0:
                other_list.remove(results[0].get('item'))

            # Remove the matched sentence from the root_list
            root_list.remove(root_list[0])
        
        # Conditions to handle unequal list sizes
        if len(root_list) > 0:
            if swapped == True:
                first_source['unsorted_{}'.format(data_type)] = other_list
            else:
                first_source['unsorted_{}'.format(data_type)] = root_list
        elif len(other_list) > 0:
            if swapped == True:
                second_source['unsorted_{}'.format(data_type)] = root_list
            else:
                second_source['unsorted_{}'.format(data_type)] = other_list
            
        return {'first_source': first_source, 'second_source': second_source}