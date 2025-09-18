from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

import uuid

Base = declarative_base()

class Verse(Base):
    __tablename__ = "verses"

    # id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    surah_number = Column(Integer, index=True)
    surah_name = Column(String, index=True)
    transliteration = Column(String, index=True)
    type = Column(String)  # Meccan / Medinan
    verse_number = Column(Integer, index=True)
    verse = Column(String)
    translation = Column(String)

    __table_args__ = (
        UniqueConstraint("surah_number", "verse_number", name="unique_surah_verse"),
    )

    def __repr__(self):
        return f"Verse(surah_number={self.surah_number}, surah_name={self.surah_name}, verse_number={self.verse_number}, verse={self.verse}, translation={self.translation})"
    
    