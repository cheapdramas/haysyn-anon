from pathlib import Path

from os import environ
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

TELEGRAM_BOT_TOKEN = environ.get("TELEGRAM_BOT_TOKEN")
