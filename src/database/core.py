from src.config import global_settings
from src.schemas.verse import Verse

from datasets import Dataset
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import IntegrityError

# DATABASE_URL="postgresql://postgres:postgres@db:5432/cleanfastapi"
DATABASE_URL = (
    f"postgresql://{global_settings.POSTGRES_USER}:{global_settings.POSTGRES_PASSWORD}"
    f"@{global_settings.POSTGRES_HOST}:{global_settings.POSTGRES_PORT}/{global_settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]

def init_db(dataset: Dataset):
    Base.metadata.create_all(bind=engine)

    # dataset = load_dataset("ReySajju742/Quran", data_files='quran-english.csv')["train"]
    # db: Session = SessionLocal()
    db: Session = get_db()

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

    # db.close()
    print(f"\n✅ Done. Inserted: {inserted}, Duplicates skipped: {duplicates}")
