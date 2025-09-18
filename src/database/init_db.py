from src.database.core import engine, SessionLocal, Base
from src.schemas.verse import Verse

from datasets import load_dataset, Dataset
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient

import uuid
import pandas as pd

def init_db(dataset: Dataset):
    Base.metadata.create_all(bind=engine)

    # dataset = load_dataset("ReySajju742/Quran", data_files='quran-english.csv')["train"]
    db: Session = SessionLocal()

    duplicates = 0
    inserted = 0
    
    print("Populating the database with verses...")
    for row in dataset:
        verse = Verse(
            surah_number=row["surah_number"],
            surah_name=row["surah_name"],
            transliteration=row["transliteration"],
            type=row["type"],
            verse_number=row["verse_number"],
            verse=row["verse"],
            translation=row["translation"],
        )
        db.add(verse)

        try:
            db.commit()
            inserted += 1
            print(f"✅ Inserted {row['surah_number']}:{row['verse_number']}")
        except IntegrityError:
            db.rollback()
            duplicates += 1
            print(f"⚠️ Skipped duplicate {row['surah_number']}:{row['verse_number']}")

    db.close()
    print(f"\n✅ Done. Inserted: {inserted}, Duplicates skipped: {duplicates}")


def ingest_dataset(qdrant_client: QdrantClient, collection_name: str, dataset: Dataset):
    """
    Ingest verses into Qdrant (run only once unless updating).
    """
    # df = pd.read_csv(dataset_path)
    # dataset = load_dataset("ReySajju742/Quran", data_files='quran-english.csv')["train"]
    points = []

    # for _, row in df.iterrows():
    for row in dataset:
        verse_id = str(uuid.uuid4())
        arabic_vec = get_embedding(row["verse"])
        trans_vec = get_embedding(row["translation"])

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

    qdrant_client.upsert(collection_name=collection_name, points=points)
    print(f"📥 Inserted {len(points)} verses into collection '{collection_name}'.")


if __name__ == "__main__":
    init_db()
