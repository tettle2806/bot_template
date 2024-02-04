from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_product_details(product_id, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_button = InlineKeyboardButton('➖', callback_data='minus')
    quan_button = InlineKeyboardButton(str(quantity), callback_data=f'quantity_{product_id}')
    plus_btn = InlineKeyboardButton('➕', callback_data='plus')
    buy_btn = InlineKeyboardButton('➕Добавить', callback_data=f'buy_{product_id}_{quantity}')
    cart_btn = InlineKeyboardButton('🛒 Корзина', callback_data='cart')
    markup.add(minus_button, quan_button, plus_btn)
    markup.add(buy_btn)
    markup.add(cart_btn)
    return markup


def generate_cart_buttons(cart_product, cart_id):
    markup = InlineKeyboardMarkup()
    # (4, 1, 'Kids-Комбо', 40000, 1)
    back = InlineKeyboardButton(text='⬅Назад', callback_data='back')
    clear = InlineKeyboardButton(text='🗑️Очистить', callback_data=f'clear_{cart_id}')
    order = InlineKeyboardButton(text='🚖Оформить заказ', callback_data=f'order_{cart_id}')
    time_order = InlineKeyboardButton(text='⌛Время доставки', callback_data=f'time')
    markup.row(back, order)
    markup.row(clear, time_order)
    for product in cart_product:
        btn1 = InlineKeyboardButton(text=f'❌{product[2]}', callback_data=f'delete_{product[2]}')
        markup.row(btn1)
    return markup


def accept_or_cancel(chat_id):
    markup = InlineKeyboardMarkup()
    accept = InlineKeyboardButton(text='✅Подтвердить заказ', callback_data=f'accept_{chat_id}')
    cancel = InlineKeyboardButton(text='❌Отменить заказ', callback_data=f'cancel_{chat_id}')
    location = InlineKeyboardButton(text='🗺️Локация', callback_data=f'location_{chat_id}')
    markup.row(accept, cancel)
    markup.row(location)
    return markup
