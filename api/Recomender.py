import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


## load data
df = pd.read_csv("Data/IMDB_top_1000.csv")
plots = df['Overview'].values.tolist()
for i in range(len(plots)):
    plots[i] = f"{plots[i]}  {df.loc[i,'Genre']}  {df.loc[i,'Director']} {df.loc[i,'Star1']} {df.loc[i,'Star2']} {df.loc[i,'Star3']} {df.loc[i,'Star4']}"

# Preprocessing 
nltk.download('punkt')
nltk.download('stopwords')

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove punctuation and stopwords, and apply stemming
    processed_tokens = [stemmer.stem(word.lower()) for word in tokens if word.isalnum() and word.lower() not in stop_words]
    
    # Join the tokens back into a single string
    return ' '.join(processed_tokens)

preprocessed_plots = [preprocess_text(plot) for plot in plots]

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit the vectorizer to the documents and transform them into TF-IDF vectors
tfidf = tfidf_vectorizer.fit_transform(preprocessed_plots)

def recomend_me(query,top_k = 1):
    movie_name = []
    movie_plot = []
    preprocessed_query = preprocess_text(query)

    tfidf_query = tfidf_vectorizer.transform([preprocessed_query])

    cos_similarities = cosine_similarity(tfidf_query,tfidf)

    sorted_idx = np.argsort(cos_similarities.squeeze())

    for idx in reversed(sorted_idx[-top_k:]):
        movie_name.append(df.loc[idx]['Series_Title'])
        movie_plot.append(plots[idx])

    return movie_name,movie_plot
