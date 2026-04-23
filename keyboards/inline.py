from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back",
            ),
            InlineKeyboardButton(text="ℹ️ Подробнее", callback_data="info"),
            InlineKeyboardButton(text="▶️ Далее", callback_data="next"),
        ],
        [InlineKeyboardButton(text="Трейлер", callback_data="treiler")],
    ]
)
