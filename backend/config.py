from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 
TEMPLATES_PATH = BASE_DIR.parent / "frontend" / "templates"
STATIC_FILES_PATH =  BASE_DIR.parent / "frontend" / "static"

class PostConfig:
	max_title_len: int = 40