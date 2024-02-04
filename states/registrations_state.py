from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    first_name = State()
    phone = State()
