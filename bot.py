import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv

load_dotenv()

logger = logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

TOKEN = os.getenv("TOKEN")

router = Router()

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот-помощник для этой группы.")


@router.message()
async def on_user_chat(message: types.Message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id != (await bot.get_me()).id:
                await message.answer(f"Привет, {new_member.full_name}! Добро пожаловать в группу!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
