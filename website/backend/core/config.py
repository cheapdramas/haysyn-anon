from pathlib import Path

from dotenv import load_dotenv
from os import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

def get_from_env(key: str) -> str:
    result = environ.get(key)
    if not result:
        print(f"Please, check your .env file: \n  {key} NOT FOUND")
        exit()
    return result

TEMPLATES_PATH = BASE_DIR / "frontend" / "templates"
STATIC_FILES_PATH =  BASE_DIR / "frontend" / "static"
DATABASE_URL = get_from_env("DATABASE_URL")
POST_SERVICE_URL = get_from_env("POST_SERVICE_URL")
POST_SERVICE_KEY = get_from_env("POST_SERVICE_KEY")
