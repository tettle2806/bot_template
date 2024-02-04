import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove

from data.loader import dp, db, bot
from states.add_item import AddItem
from .admin_keyboards.inline import accept_product
from .admin_keyboards.reply_admin import categories_buttons, admin_main


@dp.message_handler(regexp='➕Добавить товар')
async def add_item(message: Message):
    re = ReplyKeyboardRemove()
    await message.answer('Введите название товара', reply_markup=re)
    await AddItem.title.set()


@dp.message_handler(state=AddItem.title)
async def description(message: Message, state: FSMContext):
    item_name = message.text
    await state.update_data(title=item_name)
    await message.answer('Введите описание товара:\n'
                         'Пример: Картошка фри, Колбаса....\n'
                         'Ограничения 255 символов')
    await AddItem.description.set()


@dp.message_handler(state=AddItem.description)
async def cost(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer('Введите цену товара: '
                         'Формат 350000')
    await AddItem.price.set()


@dp.message_handler(state=AddItem.price)
async def select_category(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer('Выберите категорию товара',
                         reply_markup=categories_buttons())
    await AddItem.category.set()


@dp.message_handler(state=AddItem.category)
async def photo(message: Message, state: FSMContext):
    re = ReplyKeyboardRemove()
    category = message.text.split('🛟')[1]
    category_id = db.get_id_by_categories(category)[0]
    await state.update_data(category=category_id)
    await message.answer('Отправьте фото товара:',
                         reply_markup=re)
    await AddItem.photo.set()


@dp.message_handler(state=AddItem.photo, content_types=ContentType.PHOTO)
async def save_all_informations(message: Message, state: FSMContext):
    file_name = message.photo[-1].file_id
    await state.update_data(photo=file_name)
    await AddItem.accept.set()
    print(file_name)
    inf = await state.get_data('test1')
    print(inf)
    title = inf['title']
    descript = inf['description']
    price = inf['price']
    category = inf['category']
    category_name = db.get_category_by_id(category_id=category)[0]
    print(category_name)
    foto = inf['photo']
    validation_product = f'Название товара: {title}\n' \
                         f'Описание товара: {descript}\n' \
                         f'Категория товара: {category, category_name}\n' \
                         f'Цена товара: {price}'
    chat_id = message.chat.id
    await bot.send_photo(chat_id=chat_id,
                         photo=foto,
                         caption=validation_product,
                         reply_markup=accept_product())


@dp.callback_query_handler(lambda call: 'answer_' in call.data, state=AddItem.accept)
async def accept(call: CallbackQuery, state: FSMContext):
    await state.update_data(accept=call.data)
    chat_id = call.message.chat.id
    if call.data == 'answer_yes':

        inf = await state.get_data('test1')
        title = inf['title']
        descript = inf['description']
        price = inf['price']
        category = inf['category']
        foto = inf['photo']
        try:
            db.insert_alone_product(product_title=title,
                                    description=descript,
                                    price=price,
                                    image=foto,
                                    category_id=category)
            await bot.send_message(chat_id=chat_id,
                                   text='Добавление товара прошло успешно!',
                                   reply_markup=admin_main())
        except sqlite3.IntegrityError as err:
            await bot.send_message(chat_id=chat_id,
                                   text='Такой товар уже существует',
                                   reply_markup=admin_main())
        await state.finish()
    else:
        await bot.send_message(chat_id=chat_id,
                               text='Вы отменили добавление товара',
                               reply_markup=admin_main())
