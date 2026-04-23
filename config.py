import os
from dotenv import load_dotenv

load_dotenv()

KINOPOISK_API_KEY = os.getenv("API_KEY")
if not KINOPOISK_API_KEY:
    raise ValueError("API-ключ для Кинопоиска не задан в .env")

BOT_TOKEN = os.getenv("TOKEN")
