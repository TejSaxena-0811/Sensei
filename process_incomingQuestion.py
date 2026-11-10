import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib  # joblib is commonly used in ML to save trained models and speed up computations using parallel processing.
import requests


df = joblib.load("embeddings.joblib")


def create_embedding(text_list):  # just takes in text, and returns its numerical representation
    r = requests.post("http://localhost:11434/api/embed" , json={
        "model": "bge-m3",  # ollama embedding model that converts human text to numerical vectors
        "input": text_list
    })

    # print(r.json())

    embedding = r.json()['embeddings']  # r.json() converts the API response to a python dictionary
    return embedding


def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate" , json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    # print(response)
    return response


incoming_query = input("ask a question: ")
question_embedding = create_embedding([incoming_query])[0]  # putting [incoming_query] inside a list, cuz create_embeddings function accepts a list.
# print(question_embedding)

# at this point, i have both embeddings of all lecture chunks, and embeddings of the input question. so next step is to compare them using cosine similarity.

# find similarity of question_embedding with other embeddings:
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

# print(similarities)
top_results = 5  # top 5 relevant chunks
max_indices = similarities.argsort()[::-1][0:top_results]
# print(max_indices)
new_df = df.loc[max_indices]
# print(new_df[["title" , "number" , "text"]])



prompt = f''' here are video subtitle chunks containing video title, video number, the text at that time, start time in seconds, end time in seconds:

{new_df[["title" , "number" , "text" , "start" , "end"]].to_json(orient="records")}
---------------------------------------------------------

"{incoming_query}"

the user asked this question related to the video chunks, you have to answer in a human way (don't mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. if the user asks unrelated questions, tell them that you can only answer questions related to the course.
'''

with open("prompt.txt" , "w") as f:
    f.write(prompt)


response = inference(prompt)["response"]
print(response)


with open("response.txt" , "w") as f:
    f.write(response)

# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])