import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, Update

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import uvicorn

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

router = Router()
bot = Bot(token=TOKEN)
dp = Dispatcher()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот-помощник для этой группы.")


@router.message()
async def on_user_chat(message: types.Message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id != (await bot.get_me()).id:
                await message.answer(f"Привет, {new_member.full_name}! Добро пожаловать в группу!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Запуск приложения...")
    dp.include_router(router)
    
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        logger.info(f"Регистрируем вебхук: {render_url}")
        webhook_url = f"{render_url}/webhook"
        logger.info(f"Установка вебхука: {webhook_url}")
        await bot.set_webhook(webhook_url)
    else:
        logger.warning("RENDER_EXTERNAL_URL не установлен. Бот будет работать в режиме polling.")
    
    yield
    
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Приложение остановлено.")
    
app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
