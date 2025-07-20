from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 
templates_path = BASE_DIR.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=templates_path)