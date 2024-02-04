from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery

from data.loader import dp, db
from states.mailing import BotMailing
from .admin_keyboards.reply_admin import admin_main


@dp.message_handler(text='✉️Рассылка')
async def start_mailing(message: Message):
    remove = ReplyKeyboardRemove()
    await message.answer(f'Введите текст рассылки', reply_markup=remove)
    await BotMailing.text.set()


@dp.message_handler(state=BotMailing.text)
async def mailing_text(message: Message, state: FSMContext):
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
                                          InlineKeyboardButton(text='Далее', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await BotMailing.state.set()


@dp.callback_query_handler(text='next', state=BotMailing.state)
async def start_no_photo(call: CallbackQuery, state: FSMContext):
    # [(660515831,), (5488702955,)]
    users = db.select_all_id()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(text=text, chat_id=user[0])

        except Exception:
            pass

    await call.message.answer('Рассылка выполнена успешно!')


@dp.callback_query_handler(text='add_photo', state=BotMailing.state)
async def add_photo(call: CallbackQuery):
    await call.message.answer('Пришлите фото')
    await BotMailing.photo.set()


@dp.message_handler(state=BotMailing.photo, content_types=ContentType.PHOTO)
async def mailing_phot(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Далее', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.callback_query_handler(text='next', state=BotMailing.photo)
async def start(call: CallbackQuery, state: FSMContext):
    # [(660515831,), (5488702955,)]
    users = db.select_all_id()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(photo=photo, caption=text, chat_id=user[0])
        except Exception:
            pass
    await state.finish()
    await call.message.answer('Рассылка выполнена успешно!', reply_markup=admin_main())


@dp.message_handler(state=BotMailing.photo)
async def no_photo(message: Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])

    await message.answer('Пришли мне фотографию', reply_markup=markup)


@dp.callback_query_handler(state=[BotMailing.text, BotMailing.photo, BotMailing.state], text='quit', )
async def quit_key(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('Рассылка отменена')
