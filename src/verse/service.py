from src.schemas.verse import Verse
from sqlalchemy.orm import Session

def get_verse_by_id(db: Session, verse_id: str):
    return db.query(Verse).filter(Verse.id == verse_id).first()

def get_verses_by_surah_number(db: Session, surah_number: int):
    return db.query(Verse).filter(Verse.surah_number == surah_number).all()

def get_verses_by_surah_name(db: Session, surah_name: str):
    return db.query(Verse).filter(Verse.surah_name == surah_name).all()
