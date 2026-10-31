import zipfile
import json
from pathlib import Path
from bs4 import BeautifulSoup
import lxml
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from collections import defaultdict
import sys
import os

import nltk
nltk.download('punkt')

stemmer = PorterStemmer()
unique_token_threshold = 10000
index_num = 1

def main():
    partial_index = {}
    doc_id_index = {}
    doc_id = 1

    entries = []
    for root, dirs, files in os.walk('./DEV'):
        for file in files:
            if file.endswith('.json'):
                entries.append(os.path.join(root, file))

    print(len(entries))
    
    for entry in entries:
        process_doc(entry, doc_id, partial_index)
        construct_doc_index(entry, doc_id, doc_id_index)
        doc_id += 1
        if doc_id % 1000 == 0:
                print(f'Processed {doc_id} docs')

    dump_to_json(doc_id_index, "doc_id_index")

def construct_doc_index(entry, doc_id, doc_id_index):
    json_dict = open_json(entry)
    url = json_dict['url'] 
    doc_id_index[doc_id] = url

def process_doc(entry, doc_id, partial_index):
    json_dict = open_json(entry)    
    content = json_dict['content']
    tokens = tokenize_and_stem(content, stemmer)
    
    for token in tokens:
        if token not in partial_index:
            partial_index[token] = {doc_id: 1}
        else:
            if doc_id not in partial_index[token]:
                partial_index[token][doc_id] = 1
            else:
                partial_index[token][doc_id] += 1

    # Reset partial index
    if len(partial_index) >= unique_token_threshold:
        global index_num
        dump_partial_to_json(partial_index, index_num)
        partial_index.clear()
        index_num += 1

def dump_partial_to_json(partial_index, file_num):
    folder_name = 'partial_indeces'
    os.makedirs(folder_name, exist_ok=True)
    filename = f"{folder_name}/index{file_num}.json"
    with open(filename, 'w') as file:
        json.dump(partial_index, file)

def open_json(file_path):
    json_file_path = file_path
    try:
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
        return json_data
    
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: JSON decoding failed.")
    except Exception as e:
        print("Error Occurred:" , str(e))

def tokenize_and_stem(text, stemmer):
    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()
    tokens = [tok.lower() for tok in word_tokenize(text) if tok.isalnum()]
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def merge(folder_path):
    merged_index = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                partial_index = json.load(file)

            for token, doc_freq in partial_index.items():
                if token not in merged_index:
                    merged_index[token] = doc_freq
                else:
                    for doc_id, freq in doc_freq.items():
                        if doc_id in merged_index[token]:
                            merged_index[token][doc_id] += freq
                        else:
                            merged_index[token][doc_id] = freq
    return merged_index

def dump_to_json(index, mode):
    if mode == "inverted":
        filename = f"inverted_index.json"
    else:
        filename = f"doc_id_index.json"

    with open(filename, 'w') as file:
        json.dump(index, file)

if __name__ == "__main__":
    main()
    inverted_index = merge('partial_indices')
    dump_to_json(inverted_index, "inverted")

    print("DONE")