import logging

from aiogram import Dispatcher

from data.config import admin_id


async def on_startup_notify(dp: Dispatcher):
    for admin in admin_id:
        try:
            text = 'Бот запущен'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
