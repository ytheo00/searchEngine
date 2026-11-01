import json
from pathlib import Path
from nltk.stem import PorterStemmer
import time
import sys
from math import log
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re

stemmer = PorterStemmer()

def process_query(query_tokens, inverted_index):
    tfidf_dict = calculate_tfidf(query_tokens, inverted_index)
    tfidf_matrix, doc_ids = get_vsm(tfidf_dict)
    
    query_vector = tfidf_matrix[-1]
    document_vectors = tfidf_matrix[:-1]
    cosine_scores = cosine_sim(query_vector, document_vectors)
    cosine_sim_dict = dict(zip(doc_ids, cosine_scores))
    
    sorted_ranks = sorted(cosine_sim_dict, key = lambda x: cosine_sim_dict[x], reverse=True)
    return sorted_ranks

def cosine_sim(query_vect, doc_vects):
    dot_products = np.dot(doc_vects, query_vect)
    return dot_products

def get_vsm(tfidf_dict):
    doc_id_query = set()
    for term in tfidf_dict:
        for doc_id in tfidf_dict[term].keys():
            if doc_id != 'query':
                doc_id_query.add(int(doc_id))
            else:
                doc_id_query.add(doc_id)

    doc_id_query = sorted(doc_id_query, key=lambda x: (isinstance(x, str), x))
    doc_id_query = [int(i) if isinstance(i, int) else i for i in doc_id_query]
    
    unique_terms = set(tfidf_dict.keys())

    tfidf_matrix = np.zeros((len(doc_id_query), len(unique_terms)))

    term_to_index = {term: index for index, term in enumerate(unique_terms)}
    doc_id_to_index = {docID: index for index, docID in enumerate(doc_id_query)}\

    for term, doc_scores in tfidf_dict.items():
        term_index = term_to_index[term]
        for docID, score in doc_scores.items():
            try:
                doc_index = doc_id_to_index[int(docID)]
            except ValueError:
                doc_index = doc_id_to_index[docID]
            tfidf_matrix[doc_index, term_index] = score

    return tfidf_matrix, doc_id_query[:-1]

def calculate_tfidf(query_tokens, inverted_index):
    query_tf = {term: query_tokens.count(term) for term in query_tokens}
    
    tf_dict = dict()
    for term in query_tokens:
        if term not in tf_dict:
            tf_dict[term] = dict()

        tf_dict[term]['query'] = query_tf[term]

        if term in inverted_index:
            for doc_id, tf in inverted_index[term].items():
                if doc_id not in tf_dict[term]:
                    tf_dict[term][doc_id] = tf
                else:
                    tf_dict[term][doc_id] += tf
    
    df_dict = {term: len(doc_tf) for term, doc_tf in tf_dict.items()}
    
    idf_dict = {term: log((N + 1) / df) for term, df in df_dict.items()}

    tfidf_dict = dict()
    for term, doc_tf in tf_dict.items():
        tfidf_dict[term] = dict()
        for doc_id, tf in doc_tf.items():
            tfidf = (1 + log(tf)) * idf_dict[term]
            tfidf_dict[term][doc_id] = tfidf

    return tfidf_dict

def get_input():
    user_input = input("Please enter your query here: \n")
    print()
    if user_input.strip():
        input_tokens = user_input.lower().split()
        filtered_tokens = [token for token in input_tokens if token not in stopwords.words('english')]
        stem_tokens = [stemmer.stem(token) for token in filtered_tokens]
        return stem_tokens
    else:
        print("Cannot process empty query, please try again \n")
        get_input()

def display_top_10(doc_id_index, sorted_ranked_docs: list):
    print("Search results:")
    for i in range(min(len(sorted_ranked_docs), 10)):
        print(f"{i + 1}. {doc_id_index[str(sorted_ranked_docs[i])]}")

def get_file(*args):
    inverted_index = {}
    for arg in args:
        for words in arg:
            file_char = words[0]
            if re.match(r'^[a-zA-Z0-9]$', file_char):
                with open("dictionary_files/" + file_char + "_dictionary.json", "r") as file:
                    invert_index = json.load(file)
            else:
                with open("dictionary_files/special_characters_dictionary.json", "r") as file:
                    invert_index = json.load(file)
            inverted_index.update(invert_index)
    return inverted_index

if __name__ == "__main__":
    with open("doc_id_index.json", "r") as file:
        doc_id_index = json.load(file)

    global N
    N = len(doc_id_index)

    query_tokens = get_input()
    inverted_index = get_file(query_tokens)
    start = time.perf_counter()
    sorted_ranked_docs = process_query(query_tokens, inverted_index)
    display_top_10(doc_id_index, sorted_ranked_docs)
    finish = time.perf_counter()
    print(f"Finished in {round((finish - start) * 1000, 2)} ms")