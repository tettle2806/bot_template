from data.loader import dp, db
from aiogram.types import Message
from .admin_keyboards.reply_admin import middlewares_status, admin_main

@dp.message_handler(regexp='🤖Бот')
async def on_off(message: Message):
    await message.answer('Включит/Выключить', reply_markup=middlewares_status())


@dp.message_handler(regexp='Включить')
async def on_bot(message:Message):
    db.update_status('1')
    await message.answer('Бот включен', reply_markup=admin_main())


@dp.message_handler(regexp='Отключить')
async def off_bot(message:Message):
    db.update_status('0')
    await message.answer('Бот отключен', reply_markup=admin_main())