from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import kb_googledocs, kb_menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InputGDocs(StatesGroup):
    Which = State()
    site = State()
    description = State()


class Delgoogledocs(StatesGroup):
    Whatt = State()


async def command_menu(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Запутался?)', reply_markup=kb_menu)
    await state.finish()


# @dp.message_handler(commands=['add'])
async def add_google_doc(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ссылку на какой документ ты хочешь прислать?', reply_markup=kb_googledocs)
    await InputGDocs.Which.set()
    await message.delete()


# @dp.message_handler(state=InputDocs.Which)
async def load_which(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Which'] = message.text.lower()
    await bot.send_message(message.from_user.id, 'Вышли ссылку')
    await InputGDocs.next()


async def load_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site'] = message.text.lower()
    await bot.send_message(message.from_user.id, 'Добавь коментарий')
    await InputGDocs.next()


async def add_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await sqlite_db.sql_add_googledocs(state)

    await bot.send_message(message.from_user.id, 'Сохранено', reply_markup=kb_menu)
    await state.finish()


# Удаление из БД
@dp.message_handler(commands=['del_googledoc'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери документ, который хочешь удалить', reply_markup=kb_googledocs)
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
    dp.register_message_handler(command_menu, lambda message: "Main menu" in message.text, state=InputGDocs.all_states)
    dp.register_message_handler(add_google_doc, commands=['add_googledoc'], state=None)
    dp.register_message_handler(load_which, state=InputGDocs.Which)
    dp.register_message_handler(load_file, state=InputGDocs.site)
    dp.register_message_handler(add_comment, state=InputGDocs.description)

    dp.register_message_handler(load_what_del, state=Delgoogledocs.Whatt)