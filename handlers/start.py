from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот-помощник для этой группы.")


@router.message()
async def on_user_chat(message: types.Message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id != (await message.get_me()).id:
                await message.answer(f"Привет, {new_member.full_name}! Добро пожаловать в группу!")
