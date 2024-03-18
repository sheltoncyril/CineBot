import os

from sentence_transformers import SentenceTransformer

use_cuda = True if os.getenv("CUDA_ENABLED") else False
model = SentenceTransformer(
    "paraphrase-MiniLM-L6-v2",
    device=None if not use_cuda else "cuda",
    cache_folder=".models_cache",
)
