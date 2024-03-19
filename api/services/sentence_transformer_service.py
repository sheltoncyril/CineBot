import json
import os
import pickle
from collections import Counter

from base_service import BaseService
from sentence_transformers import SentenceTransformer, util


class STSvc(BaseService):
    def __init__(self):
        self._cuda_enabled = True if os.getenv("CUDA_ENABLED") else False
        self._cache_dir = True if os.getenv("SENT_TRANS_CACHE_DIR") else ".cache_dir"
        self.model = SentenceTransformer(
            "paraphrase-MiniLM-L6-v2",
            device=None if not self._cuda_enabled else "cuda",
            cache_folder=self._cache_dir,
        )
        self._embedded_corpus = list()
        self._corpus_mapped_data = list()  # recommended movie
        self._corpus = list()  # Corpus of

    def _train_from_jsonl(self, file_path=None):
        if not file_path:
            file_path = "Data/train_data.jsonl"
        with open(file_path, "r") as file:
            for line in file:
                # Load each line as JSON
                json_data = json.loads(line.strip())
                joined_text = " ".join([d["text"] for d in json_data["messages"]])
                self._corpus.append(joined_text)
                self._corpus_mapped_data.append(json_data["movieMentions"])
        self._embedded_corpus = self.model.encode(self._corpus, convert_to_tensor=True)

    def _first_run_setup(self):
        self._train_from_jsonl()
        with open(f"{self._cache_dir}/corpus_embedded.pkl", "wb") as f0, open(
            f"{self._cache_dir}/corpus_mapped_data.pkl", "wb"
        ) as f1:
            pickle.dump(self._embedded_corpus, f0)
            pickle.dump((self._corpus, self._corpus_mapped_data), f1)

    def init(self):
        if not os.path.exists(f"{self._cache_dir}/.initialized"):
            self._first_run_setup()
            with open(f"{self._cache_dir}/.initialized", mode="a"):
                pass
        with open(f"{self._cache_dir}/corpus_embedded.pkl", "rb") as f0, open(
            f"{self._cache_dir}/corpus_mapped_data.pkl", "rb"
        ) as f1:
            self._embedded_corpus = pickle.load(f0)
            self._corpus, self._corpus_mapped_data = pickle.load(f1)
        if self._cuda_enabled:
            self._embedded_corpus = util.normalize_embeddings(
                self._embedded_corpus.to("cuda")
            )

    def _retrieve_top_k_similar_queries(self, query, k=5):
        embeded_query = self.model.encode(query, convert_to_tensor=True)
        similarities = []
        for i in range(len(self._corpus)):
            sim = util.cos_sim(
                embeded_query.reshape(1, 384), self._corpus[i].reshape(1, 384)
            )
            similarities.append((sim, i))
        similarities.sort(reverse=True)  # Sort in descending order of similarity

        top_k_similar_queries = []
        for sim, idx in similarities[:k]:
            query, movie_mentions = self.query_movie_map[idx]
            top_k_similar_queries.append((idx, query, movie_mentions, sim))
        return top_k_similar_queries

    def simi_top_k(self, query, k=5):
        query_embeddings = self.model.encode(query, convert_to_tensor=True)
        if self._cuda_enabled:
            query_embeddings = query_embeddings.to("cuda")
            query_embeddings = util.normalize_embeddings(query_embeddings)
        return util.semantic_search(
            query_embeddings,
            self._embedded_corpus,
            score_function=util.dot_score,
            top_k=k,
        )[0]

    def recommend(self, query, k=3):
        similar_queries = self.simi_top_k(query, k=5)
        movie_mentions_list = []
        for similar_query in similar_queries:
            movie_mentions = self._corpus_mapped_data[similar_query["corpus_id"]]
            if movie_mentions:
                movie_mentions_list.extend(movie_mentions.values())

        # Count occurrences of each movie
        movie_mentions_counter = Counter(movie_mentions_list)

        # Find the top k most mentioned movies
        top_k_movies = movie_mentions_counter.most_common(k)

        # Extract movie titles from the top k movies
        recommended_movies = [movie for movie, _ in top_k_movies]

        return recommended_movies

    def _deprecated_recommend(self, query, k=1):
        similar_queries = self._retrieve_top_k_similar_queries(query)
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


sentence_transformer = STSvc()
sentence_transformer.init()
i = 0
while i < 15:
    print(sentence_transformer.recommend(input("Enter query: ")))
    i += 1
