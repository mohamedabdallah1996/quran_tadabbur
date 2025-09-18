from src.config import global_settings
from src.schemas.verse import Verse

from datasets import Dataset
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

class PostgresDB:
    def __init__(self, user: str, password: str, host: str, port: int, db_name: str):
        # Build DB URL
        self.DATABASE_URL = (
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )

        # Create engine and session
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def get_db(self) -> Session:
        """
        Dependency for FastAPI routes (yield session).
        """
        db: Session = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def sync_db(self):
        """
        Create tables from SQLAlchemy models.
        """
        Base.metadata.create_all(bind=self.engine)
        print("✅ Database in sync.")

    def ingest_dataset(self, dataset: Dataset):
        """
        Insert dataset rows into Postgres with duplicate handling.
        """
        db: Session = self.SessionLocal()

        duplicates = 0
        inserted = 0

        print("📥 Populating the database with verses...")
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
                # print(f"✅ Inserted {row['surah_number']}:{row['verse_number']}")
            except IntegrityError:
                db.rollback()
                duplicates += 1
                # print(f"⚠️ Skipped duplicate {row['surah_number']}:{row['verse_number']}")

        db.close()
        print(f"\n✅ Done. Inserted: {inserted}, Duplicates skipped: {duplicates}")
