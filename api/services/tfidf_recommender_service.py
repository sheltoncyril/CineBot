import os
import pickle
import ssl

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .base_service import BaseService


class TFIDFRecommenderService(BaseService):
    def __init__(self) -> None:
        cache_dir = os.getenv("CACHE_DIR")
        self._cache_dir = cache_dir if cache_dir else ".cache_dir"
        super().__init__()

    def _first_run_setup(self):
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download("punkt")
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))
        self._train_from_csv()
        with open(f"{self._cache_dir}/tfidf.pkl", "wb") as f:
            pickle.dump(
                (
                    self.df,
                    self.plots,
                    self.preprocessed_plots,
                    self.stop_words,
                ),
                f,
            )

    def _train_from_csv(self, file_path=None):
        if not file_path:
            file_path = "Data/IMDB_top_1000.csv"
        self.df = pd.read_csv(file_path)
        self.plots = self.df["Overview"].values.tolist()
        for i in range(len(self.plots)):
            self.plots[i] = (
                f"{self.plots[i]}  {self.df.loc[i,'Genre']}  {self.df.loc[i,'Director']} {self.df.loc[i,'Star1']} {self.df.loc[i,'Star2']} {self.df.loc[i,'Star3']} {self.df.loc[i,'Star4']}"  # fmt: off
            )
        self.preprocess_plots()

    def init(self, *args, **kwargs):
        self.stemmer = PorterStemmer()
        self.tfidf_vectorizer = TfidfVectorizer()
        # Fit the vectorizer to the documents and transform them into TF-IDF vectors
        if not os.path.exists(f"{self._cache_dir}/.tfidf_svc_init"):
            self._first_run_setup()
            with open(f"{self._cache_dir}/.tfidf_svc_init", mode="a"):
                pass
        with open(f"{self._cache_dir}/tfidf.pkl", "rb") as f:
            (
                self.df,
                self.plots,
                self.preprocessed_plots,
                self.stop_words,
            ) = pickle.load(f)
        self.tfidf = self.tfidf_vectorizer.fit_transform(self.preprocessed_plots)

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        processed_tokens = [self.stemmer.stem(word.lower()) for word in tokens if word.isalnum() and word.lower() not in self.stop_words]
        return " ".join(processed_tokens)

    def preprocess_plots(self):
        self.preprocessed_plots = [self.preprocess_text(plot) for plot in self.plots]

    def recommend(self, query, k=1):
        movie_name = []
        movie_plot = []
        preprocessed_query = self.preprocess_text(query)
        tfidf_query = self.tfidf_vectorizer.transform([preprocessed_query])
        cos_similarities = cosine_similarity(tfidf_query, self.tfidf)
        sorted_idx = np.argsort(cos_similarities.squeeze())
        for idx in reversed(sorted_idx[-k:]):
            movie_name.append(self.df.loc[idx]["Series_Title"])
            movie_plot.append(self.plots[idx])
        return movie_name, list(reversed(cos_similarities[0, sorted_idx[-k:]]))


if __name__ == "__main__":
    recommender = TFIDFRecommenderService()
    recommender.init()
    query = "action thriller"
    top_movies, similarities = recommender.recommend(query, top_k=3)
    for movie, similarity in zip(top_movies, similarities):
        print(f"Movie: {movie}, Similarity: {similarity}")
