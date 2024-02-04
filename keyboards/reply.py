from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.loader import db


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text='🛍 Заказать')
    review = KeyboardButton(text='✍ Оставить отзыв')
    feedback = KeyboardButton(text='☎ Связаться с нами')
    markup.row(order)
    markup.row(review, feedback)
    return markup


def generate_review():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text='⬅ Назад')
    bt1 = KeyboardButton(text='😤Хочу пожаловатся 👎🏻')
    bt2 = KeyboardButton(text='☹️Не понравилось, на 2 ⭐️⭐️')
    bt3 = KeyboardButton(text='😐Удовлетворительно на 3 ⭐️⭐️⭐️')
    bt4 = KeyboardButton(text='☺️Нормально, на 4 ⭐️⭐️⭐️⭐️')
    bt5 = KeyboardButton(text='😊Все понравилось, на 5 ❤️')
    markup.row(bt5)
    markup.row(bt4)
    markup.row(bt3)
    markup.row(bt2)
    markup.row(bt1)
    markup.row(back)
    return markup


def phone_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone = KeyboardButton(text='📞Телефон номер', request_contact=True)
    markup.add(phone)
    return markup


def generate_products(category_title):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='↙️Назад к категориям')
    cart = KeyboardButton(text='🛒 Корзина')
    products = db.get_products_by_category(category_title=category_title)
    buttons = []
    for product in products:
        btn = KeyboardButton(text=product[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(cart)
    markup.add(back)
    return markup


def generate_menu_categories():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cart = KeyboardButton(text='🛒 Корзина')
    main_mark = KeyboardButton(text='⬆️Назад')
    categories = [i[0] for i in db.get_categories()]
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category)
        buttons.append(btn)
    markup.add(*buttons, main_mark, cart)
    return markup


def send_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location = KeyboardButton(text='📍Отправить локацию', request_location=True)
    enter_location = KeyboardButton(text='Ввести локацию')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(location, enter_location)
    markup.row(back)
    return markup


def generate_type_of_order():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    delivery = KeyboardButton(text='🚖 Доставка')
    pickup = KeyboardButton(text='🏃🏻‍♂️ Самовывоз')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(delivery, pickup)
    markup.row(back)
    return markup


def type_of_pay():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    card = KeyboardButton(text='💳 Картой')
    cash = KeyboardButton(text='💸 Наличными')
    back = KeyboardButton(text='◀️ Назад')
    markup.row(card, cash)
    markup.row(back)
    return markup
