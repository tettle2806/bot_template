from aiogram.types import CallbackQuery


from data.loader import bot, dp, db
from keyboards.inline import generate_product_details, \
    generate_cart_buttons
from keyboards.reply import main_menu, generate_type_of_order, type_of_pay, generate_menu_categories


@dp.callback_query_handler(lambda call: call.data == 'plus')
async def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity < 10:
        quantity += 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_details(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Вы не можете купить бльше 10 товаров одного наименования')


@dp.callback_query_handler(lambda call: call.data == 'minus')
async def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity > 1:
        quantity -= 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_details(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Количество товаров не может равнятся 0')


@dp.callback_query_handler((lambda call: 'buy' in call.data))
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')
    product_title, price = db.get_product_by_id(product_id)
    final_price = int(quantity) * int(price)
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    try:
        '''Пытаемся закинуть новый товар в корзину'''
        db.insert_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Товар успешно добавлен в корзину''')
    except Exception as e:
        print(e)
        '''Если такой товар был то обнавляем его цену и количество'''
        db.update_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Количество успешно изменено''')


@dp.callback_query_handler(lambda call: 'cart' == call.data)
async def show_cart(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    chat_id = call.message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    # Обновить общее количество и общую сумму
    # вытащить их потом вытащить все товары в корзине
    # сформировать сообщение и отправить пользователю
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    text = '''В корзине:\n\n'''
    for cart_product in cart_products:
        text += f'{cart_product[4]} ✖️ {cart_product[2]}\n'

    type_of_order = db.select_location(telegram_id=chat_id)[0]
    if type_of_order == 'pick_up':
        order = 'Самовывоз'
        order_cost = 0
    else:
        order_cost = 15000
        order = 'Доставка'
    total_price_all = order_cost + total_price
    text += f'Товары: {total_price} сум\n' \
            f'Доставка: {order} - {order_cost} сум\n' \
            f'<b>Доставка больше 3 километров оплачивается за километр 1000 сум</b>\n' \
            f'Итого: {total_price_all} сум'
    if total_quantity == 0 or None:
        await bot.send_message(chat_id=chat_id, text='Ваша корзина пуста')
    else:
        await bot.send_message(chat_id, text, reply_markup=generate_cart_buttons(cart_products, cart_id))


@dp.callback_query_handler(lambda call: 'clear_' in call.data)
async def show_main_menu(call: CallbackQuery):
    db.delete_cart(call.from_user.id)
    db.delete_cart_products(call.data.split('_')[1])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id, text='Выберите категорию',
                           reply_markup=main_menu())


@dp.callback_query_handler(lambda call: 'order' in call.data)
async def payment(call: CallbackQuery):
    status = int(db.select_status_bot()[0])
    print(status)
    if status == 0:
        await bot.send_message(chat_id=call.from_user.id, text='Доставка временно не работает, приносим извинения')
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        chat_id = call.message.chat.id
        if db.get_cart_id(chat_id):
            cart_id = db.get_cart_id(chat_id)[0]
        else:
            db.create_cart_for_user(chat_id)
            cart_id = db.get_cart_id(chat_id)[0]
        # Обновить общее количество и общую сумму
        # вытащить их потом вытащить все товары в корзине
        # сформировать сообщение и отправить пользователю
        db.update_cart_total_price_quantity(cart_id)
        total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
        try:
            total_price, total_quantity = int(total_price), int(total_quantity)
        except:
            total_price, total_quantity = 0, 0
        cart_products = db.get_cart_products_by_cart_id(cart_id)
        phone = db.get_user_by_id(telegram_id=call.from_user.id)[2]
        text = f'''Номер заказа №{cart_id}\n
    Телефон номер: {phone}\n'''
        type_of_order = db.select_location(telegram_id=chat_id)[0]
        if type_of_order == 'pick_up':
            order = 'Самовывоз'
            order_cost = 0
        else:
            order_cost = 15000
            order = 'Доставка'
        total_price_all = order_cost + total_price
        for cart_product in cart_products:
            text += f'{cart_product[4]} ✖️ {cart_product[2]}\n'
        text += f'Товары: {total_price}\n' \
                f'Вид доставки: {order} - {order_cost}\n' \
                f'<b>Доставка больше 3 километров оплачивается за километр 1000 сум</b>\n' \
                f'Итого: {total_price_all}'
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=type_of_pay())


@dp.callback_query_handler(lambda call: 'clear' in call.data)
async def delete_cart(call: CallbackQuery):
    db.delete_cart(call.from_user.id)
    db.delete_cart_products(call.data.split('_')[1])
    await call.answer('Заказ очищен')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text='Заказ очищен', reply_markup=generate_type_of_order())


@dp.callback_query_handler(lambda call: 'delete_' in call.data)
async def delete_cart(call: CallbackQuery):
    product = call.data.split('_')[1]
    message_id = call.message.message_id
    chat_id = call.from_user.id
    cart_id = db.get_cart_id(chat_id)[0]
    db.delete_product_user(cart_id=cart_id, product=product)

    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)

    text = '''В корзине:\n\n'''
    print(total_price, total_quantity, cart_products)
    for cart_product in cart_products:
        text += f'{cart_product[4]} ✖️ {cart_product[2]}\n'
        print(cart_product)
    type_of_order = db.select_location(telegram_id=chat_id)[0]
    if type_of_order == 'pick_up':
        order = 'Самовывоз'
        order_cost = 0
    else:
        order_cost = 15000
        order = 'Доставка'
    total_price_all = order_cost + total_price
    text += f'Товары: {total_price} сум\n' \
            f'Доставка: {order} - {order_cost} сум\n' \
            f'Итого: {total_price_all} сум'
    if total_quantity == 0 or None:
        await bot.send_message(chat_id=chat_id, text='Ваша корзина пуста')
    else:
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id,
                                    reply_markup=generate_cart_buttons(cart_products, cart_id)
                                    )


@dp.callback_query_handler(lambda call: 'time' == call.data)
async def time_of_order(call: CallbackQuery):
    await call.answer(text='Время доставки от 30 до 50 минут')


@dp.callback_query_handler(lambda call: 'back' == call.data)
async def time_of_order(call: CallbackQuery):

    await bot.send_message(chat_id=call.from_user.id, text='Главное меню', reply_markup=main_menu())
    db.delete_cart(call.from_user.id)


@dp.callback_query_handler(lambda call: 'accept_' in call.data)
async def accept_order(call: CallbackQuery):
    chat_id = call.data.split('_')[1]
    cash = call.message.text + f'\n\nСтатус: Подтвержден'
    # await bot.send_message(text='Заказ подтвержден', chat_id=chat_id)
    await bot.delete_message(chat_id=-1001977700512, message_id=call.message.message_id)
    try:
        info = db.select_location(chat_id)[0]
    except:
        info = 'None'
    if info == 'pick_up':
        await bot.send_message(text=f'{cash}', chat_id=chat_id)
        await bot.send_message(chat_id=-1001977700512, text=cash)
        await bot.send_message(chat_id=chat_id, text='Заказ подтвержден')
    elif info == 'enter':
        location = "Адрес: " + db.get_enter_location(chat_id)[0]
        await bot.send_message(text=f'{cash}', chat_id=-1001977700512)
        await bot.send_message(chat_id=-1001977700512, text=location)
        await bot.send_message(chat_id=chat_id, text='Заказ подтвержден')

    elif info == 'location':
        inf = db.get_address(telegram_id=chat_id)[0]
        inf1 = inf.split(':')
        latitude = float(inf1[1].split(',')[0])
        longitude = float(inf1[2].split('}')[0])
        await bot.send_message(text=f'{cash}', chat_id=-1001977700512)
        await bot.send_location(chat_id=-1001977700512, latitude=latitude, longitude=longitude, )
        await bot.send_message(chat_id=chat_id, text='Заказ подтвержден')

    else:
        await bot.send_message(chat_id=-1001977700512, text='Данные не найдены')


    db.delete_cart(telegram_id=chat_id)


@dp.callback_query_handler(lambda call: 'cancel_' in call.data)
async def cancel_order(call: CallbackQuery):
    chat_id = call.data.split('_')[1]
    await bot.send_message(text='Заказ отменен', chat_id=chat_id)
    info = call.message.text
    db.delete_cart(telegram_id=chat_id)
    full_info = info + f'Статус: Отменен'
    await bot.send_message(chat_id=-1001977700512, text=full_info)
    message_id = call.message.message_id
    await bot.delete_message(chat_id=-1001977700512, message_id=message_id)


@dp.callback_query_handler(lambda call: 'location_' in call.data)
async def send_location_to_admin(call: CallbackQuery):
    chat_id = call.data.split('_')[1]
    try:
        info = db.select_location(chat_id)[0]
    except:
        info = 'None'
    if info == 'pick_up':
        await bot.send_message(chat_id=-1001977700512, text='Самовывоз, локации нет')
    elif info == 'enter':
        location = 'Адрес: ' + db.get_enter_location(chat_id)[0]
        await bot.send_message(chat_id=-1001977700512, text=location)
    elif info == 'location':
        inf = db.get_address(telegram_id=chat_id)[0]
        inf1 = inf.split(':')
        latitude = float(inf1[1].split(',')[0])
        longitude = float(inf1[2].split('}')[0])
        await bot.send_location(chat_id=-1001977700512, latitude=latitude, longitude=longitude)
    else:
        await bot.send_message(chat_id=-1001977700512, text='Данные не найдены')

