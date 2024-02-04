from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from data.loader import dp, db, bot
from states.delete_admins import DeleteState
from .admin_keyboards.inline import delete_product_inl
from .admin_keyboards.reply_admin import generate_products_admin, admin_main


@dp.message_handler(regexp='➖Удалить товар')
async def delete_product(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=generate_products_admin())
    await DeleteState.wait.set()


def all_product():
    product = [i[0] for i in db.get_all_products()] + ['Отменить']
    return product


@dp.message_handler(lambda message: message.text in all_product(), state=DeleteState.wait)
async def get_info_products(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.update_data(wait='wait')
        await state.finish()
        await message.answer('Вы отменили удаление', reply_markup=admin_main())
    else:
        await DeleteState.collect.set()
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
                                         reply_markup=delete_product_inl(text[0]))
            except:
                await bot.send_photo(chat_id=chat_id,
                                     photo=id_photo,
                                     caption=caption,
                                     reply_markup=delete_product_inl(text[0]))
        except:
            caption = f'Название: {text[1]}\n\nЦена: {text[3]} сум\n\n'
            await message.answer(text=caption, reply_markup=delete_product_inl(text[0]))


@dp.callback_query_handler(lambda call: 'prod_' in call.data, state=DeleteState.collect)
async def del_or_cancel(call: CallbackQuery):
    chat_id = call.message.chat.id
    print(call.data)
    if 'prod_del' in call.data:
        product_name = call.data.split('_')[2]
        print(product_name)
        db.delete_product(product_name)
        await call.answer('Товар удален')
        await bot.send_message(chat_id=chat_id,
                               text='Товар удален',
                               reply_markup=generate_products_admin())
        await DeleteState.wait.set()
    else:
        await call.answer('Действие отменено')
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        await bot.send_message(chat_id=chat_id,
                               text='Действие отменено',
                               reply_markup=generate_products_admin(),
                               )
        await DeleteState.wait.set()
