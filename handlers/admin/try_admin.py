from aiogram.types import Message

from data.config import admin_id
from data.loader import dp
from keyboards.reply import main_menu
from .admin_keyboards.reply_admin import admin_main


@dp.message_handler(text='/admin_pannel')
async def validation_admin(message: Message):
    user_id = message.from_user.id
    if user_id in admin_id:
        await message.answer('Валидация прошла успешно ваш аккаунт зарегистрирован как админ',
                             reply_markup=admin_main())
    else:
        await message.answer('Ваш аккаунт не зарегистрирован как админ',
                             reply_markup=main_menu())


@dp.message_handler(regexp='Выйти из админки')
async def exit_at_admin(message: Message):
    await message.answer('Вы вышли из админской панели',
                         reply_markup=main_menu())
