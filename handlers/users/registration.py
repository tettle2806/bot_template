import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType
from aiogram.types.message import Message

from data.loader import dp, db
from keyboards.reply import main_menu, phone_btn
from states.registrations_state import RegistrationState


@dp.message_handler(Command('register'))
async def start_registration(message: Message):
    await message.answer('Введите свое имя')
    await RegistrationState.first_name.set()


@dp.message_handler(state=RegistrationState.first_name)
async def first_name_state(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer('Отправьте номер телефона', reply_markup=phone_btn())
    await RegistrationState.phone.set()


@dp.message_handler(state=RegistrationState.phone, content_types=ContentType.CONTACT)
async def phone_state(message: Message, state: FSMContext):
    """
    Проверка номера телефона
    если номер присутствует в базе данных то операция регистрации скипается,
    если же номера телефона нет он записывается вместе с остальными данными о пользователе

    :param message:
    :param state:
    :return:
    """
    telegram_id = message.chat.id
    phone = '+' + message.contact['phone_number']
    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', str(phone))
    result2 = re.search(r'\+998\d{9}', str(phone))
    if result1 or result2:
        try:
            phone_db = db.get_colum_phone(phone)[2]
        except:
            phone_db = False
        if phone_db:
            await phone_in_db(message)
        else:
            await state.update_data(phone=phone)
            info = await state.get_data("first_name")
            first_name = info['first_name']
            phone = info['phone']
            db.full_registration(first_name, phone, telegram_id)
            await state.finish()
            await message.answer('Регистрация прошла успешно!', reply_markup=main_menu())
    else:
        await again_ask_phone(message)


async def again_ask_phone(message: Message, state=None):
    """
    Функция, которая переспрашивает номер телефона если тот был введен неверно
    :param message:
    :param state:
    :return:
    """
    await RegistrationState.phone.set()
    await message.answer('''Не верный формат телефона.
Введите номер телефона в формате: +998 ** *** ** **''')


async def phone_in_db(message: Message):
    await RegistrationState.phone.set()
    await message.answer(f'Номер телефона уже зарегистрирован!\n'
                         f'Введите другой номер телефона в формате:  +998 ** *** ** **')
