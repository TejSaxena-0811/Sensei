
# Sensei: RAG-Based-AI-Teaching-Assistant

## Live Demo of this Project on my YouTube Channel (TStack):

[Watch the Live Demo](https://www.youtube.com/watch?v=4CAsmpOXrDs)

---

# A chart explaining the complete flow:
<img width="585" height="1039" alt="image" src="https://github.com/user-attachments/assets/227e7108-2923-4d7d-8a4d-d3d7cd7789cf" />

---

## How to use this project on your own data:

### Step 1 - Collect your videos

Move all your video files to the videos folder.

### Step 2 - Convert to mp3

Convert all the video files to mp3 by ruunning video_to_mp3.

### Step 3 - Convert mp3 to json

Convert all the mp3 files to json by ruunning mp3_to_json.

### Step 4 - Convert the json files to Vectors

Use the file read_chunks.py to convert the json files to a dataframe with Embeddings and save it as a joblib pickle.

### Step 5 - Prompt generation and feeding to LLM

Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM.



## Sensei doesn't simply ask an LLM to answer from its general knowledge. It first retrieves relevant information from your own lecture collection, then the LLM converts it into an output in the English language.
