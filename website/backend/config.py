from pathlib import Path

from dotenv import load_dotenv
from os import environ


BASE_DIR = Path(__file__).resolve().parent 

load_dotenv(BASE_DIR.parent / ".env")

TEMPLATES_PATH = BASE_DIR.parent / "frontend" / "templates"
STATIC_FILES_PATH =  BASE_DIR.parent / "frontend" / "static"
DATABASE_URL = environ.get("DATABASE_URL")
