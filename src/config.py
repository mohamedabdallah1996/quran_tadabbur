from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    QDRANT_HOST: str 
    QDRANT_PORT: int

    ELASTIC_URL: str = None
    ELASTIC_PORT: str = None

    class Config:
        env_file = ".env"
        # env_file_encoding = "utf-8"


global_settings = Settings()