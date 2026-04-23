import os
from dotenv import load_dotenv

load_dotenv()

KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")

BOT_TOKEN = os.getenv("BOT_TOKEN")
