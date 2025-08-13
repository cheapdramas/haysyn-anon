from fastapi.templating import Jinja2Templates
from backend.config import TEMPLATES_PATH


templates = Jinja2Templates(directory=TEMPLATES_PATH)
