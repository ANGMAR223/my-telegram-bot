import os
from dotenv import load_dotenv

load_dotenv()

KINOPOISK_API_KEY = os.getenv("API_KEY")

BOT_TOKEN = os.getenv("TOKEN")
