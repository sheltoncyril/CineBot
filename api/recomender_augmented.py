## Recomender system based on Redial Dialogues 
import pandas as pd
import json
import numpy as np
from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load redial data
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Load each line as JSON
            json_data = json.loads(line.strip())
            data.append(json_data)
    return data

file_path = 'train_data.jsonl'
train = load_jsonl(file_path)

# Join all messages in conversation
join_convs = [''] * len(train)
i = 0
for conversation in train : 
    messages = conversation['messages']
    for message in messages:
        join_convs[i] = join_convs[i] + message['text']
    i = i + 1

print("please wait loading model")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embeded_convs = model.encode(join_convs)
print("model loaded")

def retrieve_similar_query(query):
    embeded_query = model.encode(query)
    MAX = -1
    idx = 0
    for i in range(len(embeded_convs)):
        d = cosine_similarity(embeded_query.reshape(1, 384),embeded_convs[i].reshape(1, 384))
        if d > MAX:
            MAX = d
            idx = i
    return idx,join_convs[idx],train[idx]['movieMentions']

def retrieve_top_k_similar_queries(query, k=5):
    embeded_query = model.encode(query)
    similarities = []
    for i in range(len(embeded_convs)):
        sim = cosine_similarity(embeded_query.reshape(1, 384), embeded_convs[i].reshape(1, 384))
        similarities.append((sim, i))
    similarities.sort(reverse=True)  # Sort in descending order of similarity
    
    top_k_similar_queries = []
    for sim, idx in similarities[:k]:
        top_k_similar_queries.append((idx, join_convs[idx], train[idx]['movieMentions'], sim))
    
    return top_k_similar_queries


def recommend_me_augmented(query, k=1):
    similar_queries = retrieve_top_k_similar_queries(query)
    movie_mentions_list = []
    for similar_query in similar_queries:
        movie_mentions = similar_query[2]
        movie_mentions_list.extend(list(movie_mentions.values()))

    # Count occurrences of each movie
    movie_mentions_counter = Counter(movie_mentions_list)

    # Find the top k most mentioned movies
    top_k_movies = movie_mentions_counter.most_common(k)

    # Extract movie titles from the top k movies
    recommended_movies = [movie for movie, _ in top_k_movies]

    return recommended_movies