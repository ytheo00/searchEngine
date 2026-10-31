# IR24W-A3-G19
CS121- Information Retrieval Assigment 3
-------------------------

### Group Members:

1. Daniel Lee [danijl16]
   - Student ID: 29023379
3. Josephine Ligatsyah [jligatsy]
   - Student ID: 81824675
5. Yovan Theophilus [ytheophi]
   - Student ID: 36128736
7. Peter Tumali [ptumali]
   - Student ID: 54334165

Setting up environment
----------------------

1. Create a python virtual environment on folder/repostiory
    - Input the command `python -m venv venv`
2. Install the dependencies (python libraries) from `requirements.txt`
    - Input the command `pip install -r requirements.txt`

Creating the Inverted Index
---------------------------
1. Run the python script `indexer.py`
    - Input the command `python indexer.py`
        - Which will create a folder called `\partial_indices` and will have unsorted partial indices
        - The files will then be merged together to create one main inverted index called `inverted_index.json`

Creating the Partial Index (to be used for query lookup)
--------------------------------------------------------
1. Run the python script `creating_partial_index.py`
    - Input the command `python creating_partial_index.py`
        - Which will create a folder called `dictionary_files` and will be used for query lookup

Running the search engine
-------------------------
1. Run the python script `m3_search.py`
    - Input the command `python m3_search.py`
    - It will print out an instruction to input a search query
2. Input your search query into the command prompt
3. Search results will be displayed to the user