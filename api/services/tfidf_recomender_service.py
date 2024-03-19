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
import ssl
from .base_service import BaseService

class MovieRecommender(BaseService):
    def __init__(self, data_path="Data/IMDB_top_1000.csv"):
        self.df = pd.read_csv(data_path)
        self.plots = self.df['Overview'].values.tolist()
        for i in range(len(self.plots)):
            self.plots[i] = f"{self.plots[i]}  {self.df.loc[i,'Genre']}  {self.df.loc[i,'Director']} {self.df.loc[i,'Star1']} {self.df.loc[i,'Star2']} {self.df.loc[i,'Star3']} {self.df.loc[i,'Star4']}"

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download('punkt')
        nltk.download('stopwords')

        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

        self.preprocess_plots()

        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer()

        # Fit the vectorizer to the documents and transform them into TF-IDF vectors
        self.tfidf = self.tfidf_vectorizer.fit_transform(self.preprocessed_plots)
    def innit():
        pass

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        processed_tokens = [self.stemmer.stem(word.lower()) for word in tokens if word.isalnum() and word.lower() not in self.stop_words]
        return ' '.join(processed_tokens)

    def preprocess_plots(self):
        self.preprocessed_plots = [self.preprocess_text(plot) for plot in self.plots]

    def recommend(self, query, top_k=1):
        movie_name = []
        movie_plot = []
        preprocessed_query = self.preprocess_text(query)

        tfidf_query = self.tfidf_vectorizer.transform([preprocessed_query])

        cos_similarities = cosine_similarity(tfidf_query, self.tfidf)

        sorted_idx = np.argsort(cos_similarities.squeeze())

        for idx in reversed(sorted_idx[-top_k:]):
            movie_name.append(self.df.loc[idx]['Series_Title'])
            movie_plot.append(self.plots[idx])

        return movie_name, list(reversed(cos_similarities[0, sorted_idx[-top_k:]]))


recommender = MovieRecommender()
query = "action thriller"
top_movies, similarities = recommender.recommend(query, top_k=3)
for movie, similarity in zip(top_movies, similarities):
    print(f"Movie: {movie}, Similarity: {similarity}")
