from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db


def admin_main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add = KeyboardButton(text='➕Добавить товар')
    delete = KeyboardButton(text='➖Удалить товар')
    mailing = KeyboardButton(text='✉️Рассылка')
    bot_status = KeyboardButton(text='🤖Бот')
    exit_at_admin_pannel = KeyboardButton(text='Выйти из админки')
    markup.row(add, delete)
    markup.row(mailing)
    markup.row(bot_status)
    markup.row(exit_at_admin_pannel)
    return markup


def middlewares_status():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ok = KeyboardButton(text='Включить')
    no = KeyboardButton(text='Отключить')
    markup.row(ok, no)
    return markup


def categories_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = db.get_all_categories()
    back = KeyboardButton(text='🛑 Отменить')
    buttons = []
    for categorie in categories:
        btn = KeyboardButton(text='🛟' + categorie[1])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup


def generate_products_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text='Отменить')
    products = db.get_all_products()
    buttons = []
    for product in products:
        btn = KeyboardButton(text=product[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup


def generate_menu_categories_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_mark = KeyboardButton(text='📎 Назад')
    categories = [i[0] for i in db.get_categories()]
    buttons = []
    for category in categories:
        btn = KeyboardButton(text='🔒' + category)
        buttons.append(btn)
    markup.add(*buttons, main_mark)
    return markup

