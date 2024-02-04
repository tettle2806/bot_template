from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def accept_product():
    markup = InlineKeyboardMarkup(row_width=2)
    ibt1 = InlineKeyboardButton(text='Готово',
                                callback_data='answer_yes')
    ibt2 = InlineKeyboardButton(text='Отменить',
                                callback_data='answer_no')
    markup.add(ibt1, ibt2)
    return markup


def delete_product_inl(title):
    markup = InlineKeyboardMarkup(row_width=2)
    ibt1 = InlineKeyboardButton(text='Удалить',
                                callback_data=f'prod_del_{title}')
    ibt2 = InlineKeyboardButton(text='Отменить',
                                callback_data=f'prod_cancle{title}')
    markup.add(ibt1, ibt2)
    return markup


def add_or_cancel(title):
    markup = InlineKeyboardMarkup(row_width=2)
    ibtn1 = InlineKeyboardButton(text='Добавить', callback_data=f'ad_add_{title}')
    ibtn2 = InlineKeyboardButton(text='Отменить', callback_data=f'ad_cancle_{title}')
    markup.add(ibtn1, ibtn2)
    return markup
