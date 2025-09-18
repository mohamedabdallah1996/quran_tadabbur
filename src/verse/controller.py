from src.database.core import DbSession
from src.verse import service
from src.verse.model import VerseResponse

from fastapi import APIRouter, status

router = APIRouter(
    prefix="/verses",
    tags=["verses"]
)

@router.get("/{verse_id}", response_model=VerseResponse, status_code=status.HTTP_200_OK)    
def get_verse_by_id(db: DbSession, verse_id: str):
    return service.get_verse_by_id(db, verse_id)

@router.get("/surah_number/{surah_number}", response_model=list[VerseResponse], status_code=status.HTTP_200_OK)    
def get_verses_by_surah_number(db: DbSession, surah_number: int):
    return service.get_verses_by_surah_number(db, surah_number)

@router.get("/surah_name/{surah_name}", response_model=list[VerseResponse], status_code=status.HTTP_200_OK)    
def get_verses_by_surah_name(db: DbSession, surah_name: str):
    return service.get_verses_by_surah_name(db, surah_name)