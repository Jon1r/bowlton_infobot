from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import kb_googledocs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InputDocs(StatesGroup):
    Which = State()
    file = State()
    description = State()


class Delgoogledocs(StatesGroup):
    Whatt = State()


# @dp.message_handler(commands=['add'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'What do u want?', reply_markup=kb_googledocs)
    await InputDocs.Which.set()
    await message.delete()


# @dp.message_handler(state=InputDocs.Which)
async def load_which(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Which'] = message.text
    await bot.send_message(message.from_user.id, 'Вышли документ')
    await InputDocs.next()


async def load_file(message, state: FSMContext):
    async with state.proxy() as data:
        data['file'] = message.text.lower()
    await bot.send_message(message.from_user.id, 'Добавь коментарий')
    await InputDocs.next()


async def add_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await sqlite_db.sql_add_googledocs(state)

    await state.finish()


# Удаление из БД
@dp.message_handler(commands=['del_googledoc'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери документ, который хочешь удалить', reply_markup=kb_doc)
    await Delgoogledocs.Whatt.set()
    await message.delete()


async def load_what_del(message: types.Message, state: FSMContext):
    all = await sqlite_db.sql_take_info_providers(message.text.lower())
    for row in all:
        await bot.send_message(message.from_user.id, row[0] + " - " + row[2],
                               reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(text='Delete',callback_data='del ' + row[0])))

    await state.finish()


@dp.callback_query_handler(Text(startswith='del '))
async def del_provider(callback_query: types.CallbackQuery):
    await sqlite_db.sql_del_googledocs(callback_query.data.replace('del ', ''))
    await callback_query.answer(text='Удалена', show_alert=True)


def register_handlers_admin_dc(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['add_googledoc'], state=None)
    dp.register_message_handler(load_which, state=InputDocs.Which)
    dp.register_message_handler(load_file, content_types=["document"], state=InputDocs.file)
    dp.register_message_handler(add_comment, state=InputDocs.description)

    dp.register_message_handler(load_what_del, state=Delgoogledocs.Whatt)