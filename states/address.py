from aiogram.dispatcher.filters.state import State, StatesGroup


class AddressState(StatesGroup):
    address = State()
