from pathlib import Path
from sys import exit
from os import environ
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

def get_from_env(key: str) -> str:
    result = environ.get(key)
    if not result:
        print(f"Please, check your .env file: \n  {key} NOT FOUND")
        exit()
    return result

KEY = get_from_env("KEY") 
ADMINS = get_from_env("ADMINS").split(',')
DATABASE_URL = get_from_env("DATABASE_URL")
REDIS_CHANNEL_NAME = "posts"
TELEGRAM_BOT_TOKEN = get_from_env("TELEGRAM_BOT_TOKEN")
WEBSITE_URL_BASE = get_from_env("WEBSITE_URL_BASE")
API_VERSION = get_from_env("API_VERSION")
