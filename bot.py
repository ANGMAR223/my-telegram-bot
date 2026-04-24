import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update, CallbackQuery
import traceback
from aiogram.exceptions import TelegramBadRequest

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import uvicorn

from handlers.start import router as router_start
from handlers.movies import router as router_movies

from config import BOT_TOKEN

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Запуск приложения...")
    dp.include_router(router_start)
    dp.include_router(router_movies)

    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        logger.info(f"Регистрируем вебхук: {render_url}")
        webhook_url = f"{render_url}/webhook"
        logger.info(f"Установка вебхука: {webhook_url}")
        await bot.set_webhook(webhook_url, allowed_updates=["message", "callback_query"])
    else:
        logger.warning("RENDER_EXTERNAL_URL не установлен. Бот будет работать в режиме polling.")

    yield

    await bot.session.close()
    logger.info("Приложение остановлено.")


app = FastAPI(lifespan=lifespan)


@dp.errors()
async def callback_error_handler(event, **kwargs):
    """
    Перехватывает ВСЕ ошибки, возникающие в callback-обработчиках.
    Логирует их и пытается ответить на callback, чтобы убрать "часики".
    """
    error = event.exception
    update = event.update

    logger.error(f"Ошибка при обработке обновления: {error}")
    logger.error(traceback.format_exc())

    if update and update.callback_query:
        try:
            await update.callback_query.answer()
        except Exception as e:
            logger.warning(f"Не удалось ответить на callback: {e}")
            
    return True


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
