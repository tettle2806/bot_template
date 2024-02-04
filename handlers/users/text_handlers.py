from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.message import Message

from data.config import admin_id
from data.config import type_of_review
from data.loader import dp, db, bot
from keyboards.inline import accept_or_cancel
from keyboards.inline import generate_product_details, generate_cart_buttons
from keyboards.reply import generate_review, \
    main_menu, \
    generate_type_of_order, \
    generate_menu_categories, \
    send_location, generate_products
from states.address import AddressState
from states.card_state import CardState


@dp.message_handler(regexp='🛍 Заказать')
async def reaction_order(message: Message):
    status = int(db.select_status_bot()[0])
    print(status)
    if status == 0:
        await message.answer('Доставка временно не работает, приносим извинения')
    else:
        await message.answer('Выберите вид заказа', reply_markup=generate_type_of_order())


@dp.message_handler(regexp='🚖 Доставка')
async def reaction_on_delivery(message: Message):
    await message.answer('Отправьте локацию', reply_markup=send_location())


@dp.message_handler(content_types=['location'])
async def save_location(message: Message):
    chat_id = message.chat.id
    location = str(message.location)
    db.create_cart_for_user(chat_id)
    db.insert_location(location='location', telegram_id=chat_id)
    db.insert_enter_address(telegram_id=chat_id, address=location)
    await message.answer(text='Выберите категорию', reply_markup=generate_menu_categories())


@dp.message_handler(regexp='🏃🏻‍♂️ Самовывоз')
async def reaction_on_pickup(message: Message):
    chat_id = message.from_user.id
    db.create_cart_for_user(chat_id)
    order = 'pick_up'
    db.insert_location(order, chat_id)
    await message.answer('Каталог', reply_markup=generate_menu_categories())


@dp.message_handler(regexp='✍ Оставить отзыв')
async def reaction_review(message: Message):
    await message.answer('Выберите одно', reply_markup=generate_review())


@dp.message_handler(regexp='☎ Связаться с нами')
async def reaction_feedback(message: Message):
    await message.answer('<b>Единый call-center:</b> +998951940102 или +998997639787')


@dp.message_handler(regexp='⬅ Назад')
async def reaction_back(message: Message):
    await message.answer('Главное меню', reply_markup=main_menu())


@dp.message_handler(regexp='⬆️Назад')
async def reaction_back(message: Message):
    await message.answer('Выберите вид заказа', reply_markup=generate_type_of_order())


@dp.message_handler(regexp='◀️ Назад')
async def back_to_cart(message: Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    chat_id = message.chat.id
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
            f'Итого: {total_price_all} сум'
    await bot.send_message(chat_id, text, reply_markup=generate_cart_buttons(cart_products, cart_id))


@dp.message_handler(regexp='↙️Назад к категориям')
async def reaction_back(message: Message):
    await message.answer('Категории', reply_markup=generate_menu_categories())


@dp.message_handler(lambda message: message.text in type_of_review)
async def send_review_admin(message: Message):
    id_user = message.from_user.id
    info_about_user = db.get_user_by_id(id_user)
    text = f'Имя: {info_about_user[1]}\n' \
           f'ID: {info_about_user[0]}\n' \
           f'Номер телефона: {info_about_user[2]}\n' \
           f'Отзыв: {message.text}'
    await message.answer('Ваш отзыв принят, спасибо что помогаете нам развиваться!', reply_markup=main_menu())
    await bot.send_message(chat_id=admin_id[0], text=text)


def categories():
    category = [i[0] for i in db.get_categories()]
    return category


@dp.message_handler(lambda message: message.text in categories())
async def reaction_on_category(message: Message):
    mess = message.text
    await message.answer('Выберите продукт', reply_markup=generate_products(mess))


def product():
    p = [i[0] for i in db.get_all_products()]
    return p


@dp.message_handler(lambda message: message.text in product())
async def get_info_products(message: Message):
    chat_id = message.chat.id
    text = db.get_products_by_title(message.text)
    caption = f'Название: {text[1]}\n\nОписание: {text[2]}\n\nЦена: {text[3]} сум\n\n'
    try:
        path = 'photo/' + text[4]
        id_photo = text[4]
        try:
            with open(f'{path}', mode='rb') as photo:
                await bot.send_photo(chat_id=chat_id,
                                     photo=photo,
                                     caption=caption,
                                     reply_markup=generate_product_details(text[0]))
        except:
            await bot.send_photo(chat_id=chat_id,
                                 photo=id_photo,
                                 caption=caption,
                                 reply_markup=generate_product_details(text[0]))
    except:
        caption = f'Название: {text[1]}\n\nЦена: {text[3]} сум\n\n'
        await message.answer(text=caption, reply_markup=generate_product_details(text[0]))


@dp.message_handler(regexp='Ввести локацию')
async def enter_address(message: Message):
    re = ReplyKeyboardRemove
    await message.answer('Введите адрес доставки', reply_markup=re())
    await AddressState.address.set()


@dp.message_handler(state=AddressState.address)
async def save_enter_address(message: Message, state: FSMContext):
    address = message.text
    chat_id = message.from_user.id
    await state.update_data(address=address)
    info = await state.get_data('address')
    ins_address = info['address']
    await state.finish()
    db.create_cart_for_user(chat_id)
    db.insert_location(telegram_id=chat_id, location='enter')
    db.insert_enter_address(telegram_id=chat_id, address=ins_address)
    await message.answer('Категории', reply_markup=generate_menu_categories())


@dp.message_handler(regexp='🛒 Корзина')
async def reaction_on_crt_reply(message: Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    chat_id = message.chat.id
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


@dp.message_handler(regexp='💳 Картой')
async def card_payment(message: Message):
    await message.answer(f'Оплатите заказ переводом\n'
                         f'8600570473099074\n'
                         f'Отправьте скриншот чека',
                         )

    chat_id = message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    phone = db.get_user_by_id(telegram_id=message.from_user.id)[2]
    text = f'Номер заказа №{cart_id}\n' \
           f'Телефон номер: {phone}\n'
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
            f'Итого: {total_price_all}\n\n' \
            f'Оплата: Картой\n' \
            f'Статус: Не оплачено'

    await bot.send_message(chat_id=-1001977700512, text=text, reply_markup=accept_or_cancel(chat_id))
    # await bot.send_message(chat_id=cashier[0], text=text, reply_markup=accept_or_cancel(chat_id))
    await CardState.payment.set()


@dp.message_handler(content_types=['photo'], state=CardState.payment)
async def photo_card(message: Message, state=FSMContext):
    chat_id = message.chat.id
    file_name = message.photo[-1].file_id
    await state.update_data(payment=file_name)
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except Exception as err:
        error = err
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    phone = db.get_user_by_id(telegram_id=message.from_user.id)[2]
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
            f'Итого: {total_price_all}\n\n' \
            f'Оплата: Картой\n' \
            f'Статус: Оплачено'
    await state.finish()
    await bot.send_message(chat_id=chat_id, text='Ожидайте ответа администратора', reply_markup=main_menu())
    await bot.send_photo(chat_id=-1001977700512, photo=file_name, caption=text)


@dp.message_handler(regexp='💸 Наличными')
async def cash_payment(message: Message):
    await message.answer('Заказ передан администраторам, ожидайте ответа', reply_markup=main_menu())

    chat_id = message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except Exception as err:
        error = err
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    phone = db.get_user_by_id(telegram_id=message.from_user.id)[2]
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
            f'Итого: {total_price_all}\n\n' \
            f'Оплата: Наличными'

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    await bot.send_message(chat_id=-1001977700512, text=text, reply_markup=accept_or_cancel(chat_id))

