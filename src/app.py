from src.database.engine.qdrant import QdrantDB
from src.database.engine.postgres import PostgresDB
from src.verse.controller import router as verses_router
from src.config import global_settings

from fastapi import FastAPI
from datasets import load_dataset
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load dataset 
    dataset = load_dataset("ReySajju742/Quran", data_files='quran-english.csv')["train"]
    
    # Initialize the postgres database with Quran verses 
    # init_db(dataset)
    postgres_db = PostgresDB(global_settings.POSTGRES_USER, global_settings.POSTGRES_PASSWORD, 
                             global_settings.POSTGRES_HOST, global_settings.POSTGRES_PORT, global_settings.POSTGRES_DB)
    postgres_db.sync_db()
    postgres_db.ingest_dataset(dataset)

    # Initialize Qdrant with the Quran verses embeddings 
    qdrant_db = QdrantDB(global_settings.QDRANT_HOST, port=global_settings.QDRANT_PORT)  
    qdrant_db.init_collection("quran_embeddings")
    qdrant_db.ingest_dataset(dataset, "quran_embeddings")

    yield   

app = FastAPI(lifespan=lifespan)

app.include_router(verses_router)