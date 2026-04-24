from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from services.kinopoisk import (
    get_top_movies,
    show_next_film,
    send_film_message,
    show_back_film,
    show_film_deteil,
)
import logging

from aiogram.fsm.context import FSMContext
from utils.states import MovieState


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("movies"))
async def handle_movies(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MovieState.waiting_for_movie_selection)
    logger.info(f"Пользователь {message.from_user.id} запросил топ фильмов.")
    await message.answer("Получаю список топ фильмов...")
    movies = await get_top_movies()
    if not movies:
        await message.answer("Не удалось получить список фильмов.")
        return

    logger.info(f"Получено {len(movies['items'])} фильмов от Kinopoisk API.")

    films = movies["items"]

    if not films:
        await message.answer("Не удалось получить список фильмов.")
        return

    await state.update_data(movies=films, index=0)
    await send_film_message(message, films[0])


@router.callback_query(F.data == "info")
async def info_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_film_deteil(callback, state)
    


@router.callback_query(F.data == "next")
async def next_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_next_film(callback, state)
    


@router.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_back_film(callback, state)
    
