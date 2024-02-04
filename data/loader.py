from aiogram import executor
from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from database.database import DataBase

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
db = DataBase()

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
if __name__ == '__main__':
    executor.start_polling(dp)