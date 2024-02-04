from aiogram.types import Message

from data.loader import dp, db, bot
from keyboards.reply import main_menu
from utils.misc.throttling import rate_limit
from .registration import start_registration


@rate_limit(limit=5)
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer('Добро пожаловать')
    telegram_id = message.from_user.id
    db_telegram_id = db.get_user_by_id(telegram_id)
    print(db_telegram_id)
    if db_telegram_id:
        first_name = db_telegram_id[1]
        phone = db_telegram_id[2]
        await message.answer(f'Имя: {first_name}\n'
                             f'Номер телефона: {phone}',
                             reply_markup=main_menu())
    else:
        db.first_registration(telegram_id)
        await start_registration(message)


@dp.message_handler(commands=['restart'])
async def restart_register(message: Message):
    db.drop_user_by_id(message.from_user.id)
    telegram_id = message.from_user.id
    db.first_registration(telegram_id)
    await bot.send_message(text='Данные удалены, Пройдите регистрацию заново', chat_id=message.chat.id)
    await start_registration(message)


@dp.message_handler(commands='help')
async def command_start(message: Message):
    await message.answer('<b>Единый call-center:</b> +998951940102 или +998997639787')
