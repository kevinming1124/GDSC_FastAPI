import os
from functools import lru_cache
from sqlalchemy import text
from dotenv import load_dotenv


@lru_cache()
def get_settings():
    load_dotenv( f".env.{os.getenv('APP_MODE')}")
    return Settings()

class Settings():
    app_name:str = "iThome2023 FastAPI Tutorial"
    author:str = "Kevin Ming"

    app_mode: str = os.getenv("APP_MODE")
    port:int = int(os.getenv("PORT"))
    reload:bool = bool(os.getenv("RELOAD"))

    db_type:str = os.getenv("DB_TYPE").upper()
    database_url: str = os.getenv(f"{db_type}_DATABASE_URL")