# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из файла .env, если он присутствует

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Пожалуйста, установите переменную окружения BOT_TOKEN.")


BOT_TOKEN = "7686517998:AAGSTlqu1lYxgKHuZnjvTTrHz96QuRASK2c"