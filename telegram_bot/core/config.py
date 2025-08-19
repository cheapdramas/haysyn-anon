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

POST_SERVICE_KEY = get_from_env("POST_SERVICE_KEY") 
ADMINS = get_from_env("ADMINS").split(',')
TELEGRAM_BOT_TOKEN = get_from_env("TELEGRAM_BOT_TOKEN")
WEBSOCKET_URL = get_from_env("WEBSOCKET_URL")
