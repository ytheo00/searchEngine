import json
from pathlib import Path
from nltk.stem import PorterStemmer
from collections import Counter
import time
import sys
import pickle

stemmer = PorterStemmer()


def search_for(inverted_index, *args):
    if not args: #If empty
        return []
    values = []
    combined_dict = Counter()
    for arg in args:
        if arg in inverted_index:
            postings = inverted_index[arg]
            values.append(postings)
            combined_dict += Counter(inverted_index[arg])
        else:
            raise ValueError(f"Token '{arg}' not found in the dictionary")
        
    document_ids = sorted(set(values[0]).intersection(*values[1:]), key=lambda x: combined_dict[x], reverse=True)
    
    return document_ids


def get_token_words():
    user_input = input("Enter search query: ")
    #Stem the user_input first with Porter stem
    if user_input:
        token_words = user_input.lower().split(' ')
        stem_tokens = [stemmer.stem(token) for token in token_words]
        return stem_tokens
    else:
        return []

def find_document_ids(document_ids):
    if not document_ids:
        print("No common document IDs to display.")
    else:
        top5 = []
        print("Common document IDs:")
        if len(document_ids) >= 5:
            for i in range(0, 5):
                top5.append(document_ids[i])
        else:
            for i in range(0, len(document_ids)):
                top5.append(document_ids[i])
    return(top5)
            
def display_urls(document_id):
    with open ("doc_id_index.json", 'r') as file:
        data = json.load(file)     
    for i in range(0, len(document_id)):
        print(f"{i+1}. {data[document_id[i]]}\n")

    
if __name__ == "__main__":
    with open ("inverted_index.json", 'r') as file:
        data = json.load(file)    
    token_words = get_token_words()
    document_ids = search_for(data, *token_words)
    top_results = find_document_ids(document_ids)
    display_urls(top_results)