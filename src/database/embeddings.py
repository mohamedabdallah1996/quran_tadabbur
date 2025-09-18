from typing import List, Union
from sentence_transformers import SentenceTransformer

import numpy as np

class EmbeddingsModel:
    def __init__(self, model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize the embeddings service.
        :param model: Model name to load.
        """
        self.model = SentenceTransformer(model)
        
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for given text(s).
        :param texts: Single string or list of strings.
        :return: np.ndarray of embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]

        return np.array(self.model.encode(texts))

    def compare(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Compare two embeddings with cosine similarity.
        :param emb1: First embedding.
        :param emb2: Second embedding.
        :return: similarity score (0-1).
        """
        return self.model.similarity(emb1, emb2)
