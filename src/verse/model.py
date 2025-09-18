from pydantic import BaseModel
from uuid import UUID


class VerseBase(BaseModel):
    surah_number: int
    surah_name: str
    transliteration: str
    type: str
    verse_number: int
    verse: str
    translation: str


class VerseResponse(VerseBase):
    id: UUID

    class Config:
        orm_mode = True
