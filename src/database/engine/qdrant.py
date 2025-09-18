from src.database.embeddings import EmbeddingsModel

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from datasets import Dataset

import uuid


class QdrantDB:
    def __init__(self, host: str, port: int, embeddings_model: EmbeddingsModel, embedding_dim: int = 1024):
        self.client = QdrantClient(host=host, port=port)
        self.embeddings_model = embeddings_model
        self.embedding_dim = embedding_dim  # adjust if you change model size

    def init_collection(self, collection_name: str):
        """
        Create collection if it does not exist.
        """
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "arabic_verse_vector": VectorParams(size=self.embedding_dim, distance=Distance.COSINE),
                    "verse_translation_vector": VectorParams(size=self.embedding_dim, distance=Distance.COSINE),
                },
            )
            print(f"✅ Collection '{collection_name}' created.")
        else:
            print(f"ℹ️ Collection '{collection_name}' already exists.")

    def ingest_dataset(self, dataset: Dataset, collection_name: str):
        """
        Ingest verses into Qdrant (run only once unless updating).
        """
        # dataset = load_dataset("ReySajju742/Quran", data_files='quran-english.csv')["train"]
        points = []

        for row in dataset:
            verse_id = str(uuid.uuid4())
            arabic_vec = self.embeddings_model.embed(row["verse"])
            trans_vec = self.embeddings_model.embed(row["translation"])

            point = PointStruct(
                id=verse_id,
                vector={
                    "arabic_vector": arabic_vec,
                    "translation_vector": trans_vec,
                },
                payload={
                    "surah_number": int(row["surah_number"]),
                    "surah_name": row["surah_name"],
                    "verse_number": int(row["verse_number"]),
                    "verse": row["verse"],
                    "translation": row["translation"],
                },
            )
            points.append(point)

        self.client.upsert(collection_name=collection_name, points=points)
        print(f"📥 Inserted {len(points)} verses into collection '{collection_name}'.")


    def search(self, query: str, collection_name: str, lang: str = "translation", top_k: int = 5):
        """
        Search verses by query embedding.
        lang: 'translation' or 'arabic'
        """
        query_vector = self.embeddings_model.embed(query)

        results = self.client.search(
            collection_name=collection_name,
            query_vector=(f"{lang}_vector", query_vector),
            limit=top_k,
        )

        return [
            {
                "surah_name": r.payload["surah_name"],
                "surah_number": r.payload["surah_number"],
                "verse_number": r.payload["verse_number"],
                "verse": r.payload["verse"],
                "translation": r.payload["translation"],
                "score": r.score,
            }
            for r in results
        ]
