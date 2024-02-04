from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteState(StatesGroup):
    wait = State()
    collect = State()
