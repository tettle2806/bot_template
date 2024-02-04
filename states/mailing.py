from aiogram.dispatcher.filters.state import State, StatesGroup


class BotMailing(StatesGroup):
    text = State()
    state = State()
    photo = State()
