import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib



def create_embedding(text_list):  # just takes in text, and returns its numerical representation
    r = requests.post("http://localhost:11434/api/embed" , json={
        "model": "bge-m3",  # ollama embedding model that converts human text to numerical vectors
        "input": text_list
    })

    # print(r.json())

    embedding = r.json()['embeddings']  # r.json() converts the API response to a python dictionary
    return embedding


my_dicts = []
chunk_id = 0
jsons = os.listdir("new_jsons")
# print(jsons)

for json_file in jsons:
    with open(f"new_jsons/{json_file}") as f:
        content = json.load(f)

    print(f"Creating embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])  # in the json files, every chunk has text in it. that text is brought together in a single list and given as an argument to the function. then, embeddings are generated for each list element (each list element being the text of each individual chunk).
    for i, chunk in enumerate(content["chunks"]):
        # print(chunk)
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)

print(my_dicts)  # my_dicts contains all the lecture chunks from all json files, with their metadata and embeddings attached.

df = pd.DataFrame.from_records(my_dicts)
# print(df)

# saving this dataframe: (embeddings.joblib is the file where the dataframe is saved)
joblib.dump(df , "embeddings.joblib")  # saving the dataframe (and loading it later in process_incoming.py), so that embeddings are not generated every time i ask a question. generating embeddings becomes a one time thing, which saves a lot of processing time. if later theres some change in data, i will delete the current embeddings.joblib, and run this file to create the embeddings again.
