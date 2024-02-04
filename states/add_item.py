from aiogram.dispatcher.filters.state import State, StatesGroup


class AddItem(StatesGroup):
    title = State()
    description = State()
    price = State()
    category = State()
    photo = State()
    accept = State()