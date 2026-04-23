import httpx
from config import KINOPOISK_API_KEY
import random
import asyncio
from aiogram.fsm.context import FSMContext
from keyboards.inline import settings
from aiogram.types import CallbackQuery, InputMediaPhoto


async def get_top_movies():
    random_page = random.randint(1, 35) 
    url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/collections?type=TOP_POPULAR_ALL&page={random_page}"

    headers = {"X-API-KEY": KINOPOISK_API_KEY, "Content-Type": "application/json"}
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data


async def send_film_message(message, film):
    title = film.get("nameRu") or film.get("nameEn") or "Без названия"
    rating = film.get("ratingKinopoisk", "Нет рейтинга")
    year = film.get("year", "Год неизвестен")
    poster_url = film.get("posterUrl", "")
    description = (
        film.get("description")[:50] + "..." if film.get("description") else "Описание отсутствует"
    )

    if poster_url:
        await message.answer_photo(
            photo=poster_url,
            caption=f"{title} ({year}) - Рейтинг: {rating}\n\n{description}",
            reply_markup=settings,
        )
    else:
        await message.answer(
            f"{title} ({year}) - Рейтинг: {rating}\n\n{description}", reply_markup=settings
        )


async def show_film(callback: CallbackQuery, films: dict):
    film = films
    title = film.get("nameRu") or film.get("nameEn") or "Без названия"
    rating = film.get("ratingKinopoisk", "Нет рейтинга")
    year = film.get("year", "Год неизвестен")
    poster_url = film.get("posterUrl", "")
    description = (
        film.get("description")[:50] + "..." if film.get("description") else "Описание отсутствует"
    )

    media = InputMediaPhoto(
        media=poster_url, caption=f"{title} ({year}) - Рейтинг: {rating}\n\n{description}"
    )

    if poster_url:
        await callback.message.edit_media(media, reply_markup=settings)
    else:
        await callback.message.edit_caption(
            f"{title} ({year}) - Рейтинг: {rating}\n\n{description}", reply_markup=settings
        )


async def show_next_film(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    films = data["movies"]
    index = data["index"]
    if index < len(films) - 1:
        index += 1
        await state.update_data(index=index)
        await show_film(callback, films[index])
    else:
        await callback.answer(
            "На данной странице нет больше фильмов. Воспользуйтесь '/movies'", show_alert=True
        )
        await show_film(callback, films[index])


async def show_back_film(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    films = data["movies"]
    index = data["index"]
    if index > 0:
        index -= 1
        await state.update_data(index=index)
        await show_film(callback, films[index])
    else:
        await callback.answer("Эй, чукча, это первый фильм в списке, жми 'Далее'", show_alert=True)
        await show_film(callback, films[index])


async def show_film_deteil(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    films = data["movies"]
    index = data["index"]
    film = films[index]
    title = film.get("nameRu") or film.get("nameEn") or "Без названия"
    rating = film.get("ratingKinopoisk", "Нет рейтинга")
    year = film.get("year", "Год неизвестен")
    poster_url = film.get("posterUrl", "")
    description = (
        film.get("description") + "..." if film.get("description") else "Описание отсутствует"
    )
    age = film.get("ratingAgeLimits")
    if age:
        age = f'{age[3:]}+'
    else:
        age = "Без возрастного рейтинга"

    caption = f"{title} ({year}) - Рейтинг: {rating}\nВозрастной рейтинг - {age}\n\n{description}"

    media = InputMediaPhoto(media=poster_url, caption=caption)

    if poster_url:
        await callback.message.edit_media(media, reply_markup=settings)
    else:
        await callback.message.edit_caption(
            f"{title} ({year}) - Рейтинг: {rating}\n\n{description}", reply_markup=settings
        )
