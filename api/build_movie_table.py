import json
import pandas as pd

# This code build the movie_data table which consist of 3 columns : 
# - Movie title
# - Movie Id
# - text : concatenation of every conversation that mentioned the movie in the Redial dataset


def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Load each line as JSON
            json_data = json.loads(line.strip())
            data.append(json_data)
    return data

file_path = 'train_data.jsonl'
train = load_jsonl('train_data.jsonl')
test = load_jsonl('test_data.jsonl')

movie_table = {'movie_title': [], 'movie_id': [], 'text': []}

# Function to replace movie IDs with movie titles
def replace_movie_ids(text, movie_mentions):
    for movie_id, movie_title in movie_mentions.items():
        text = text.replace('@' + movie_id, movie_title)
        return text

for i in range(len(train)):
    conv = train[i]
    movies = conv['movieMentions']
    if isinstance(movies, dict):
        messages = conv['messages']
        join = ''
        for message in messages:
            join += " " + message['text']
        for movie_id in movies:
            if movie_id not in movie_table['movie_id']:
                movie_table['movie_title'].append(movies[movie_id])
                movie_table['movie_id'].append(movie_id)
                movie_table['text'].append(join)  # Append as a list
            else: 
                movie_table['text'][movie_table['movie_id'].index(movie_id)] += ' ' + join

df = pd.DataFrame(movie_table)

df.to_csv('Data/movie_data.csv', index=False)


