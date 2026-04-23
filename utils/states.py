from aiogram.fsm.state import State, StatesGroup


class MovieState(StatesGroup):
    waiting_for_movie_selection = State()
