from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import kb_in_del_providers, kb_providers, kb_produces, kb_parts, kb_electrica, kb_hardware, kb_menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Providers(StatesGroup):
    type = State()
    Whatt = State()
    Wheree = State()
    Comment = State()


class DELproviders(StatesGroup):
    type = State()
    Whatt = State()


async def command_menu(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Запутался?)', reply_markup=kb_menu)
    await state.finish()


@dp.message_handler(commands=['add_providers'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'What do u want?', reply_markup=kb_providers)
    await Providers.type.set()
    await message.delete()


async def cm_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text.lower()
    if message.text == 'Electrica':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь добавить?',
                               reply_markup=kb_electrica)
    elif message.text == 'Hardware':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь добавить?',
                               reply_markup=kb_hardware)
    elif message.text == 'Parts':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь добавить?',
                               reply_markup=kb_parts)
    elif message.text == 'Produces':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь добавить?',
                               reply_markup=kb_produces)
    await Providers.next()


# @dp.message_handler(state=FSMAdmin.What)
async def load_what(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Whatt'] = message.text.lower()
    await Providers.next()
    await message.reply('Скинь ссылку на этот компонент')


# @dp.message_handler(state=FSMAdmin.Where)
async def load_where(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Wheree'] = message.text
    await Providers.next()
    await message.reply('Напиши краткое описание этого поставщика')


# @dp.message_handler(state=FSMAdmin.Comment)
async def load_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Comment'] = message.text
    await sqlite_db.sql_add_providers(state)
    await message.answer('Запомнил', reply_markup=kb_menu)

    await state.finish()


# Удаление из БД
@dp.message_handler(commands=['del_providers'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери тип закупки', reply_markup=kb_providers)
    await DELproviders.type.set()
    await message.delete()


async def cm_delete(message: types.Message, state: FSMContext):
    if message.text == 'Electrica':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь удалить?',
                               reply_markup=kb_electrica)
    elif message.text == 'Hardware':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь удалить?',
                               reply_markup=kb_hardware)
    elif message.text == 'Parts':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь удалить?',
                               reply_markup=kb_parts)
    elif message.text == 'Produces':
        await bot.send_message(message.from_user.id,
                               'Какой компонент ты хочешь удалить?',
                               reply_markup=kb_produces)
    await DELproviders.next()


async def load_what_del(message: types.Message, state: FSMContext):
    all = await sqlite_db.sql_take_info_providers(message.text.lower())
    for row in all:
        await bot.send_message(message.from_user.id, row[2] + " - " + row[3],
                               reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(text='Delete',callback_data='pdel ' + row[2])))

    await state.finish()


@dp.callback_query_handler(Text(startswith='pdel '))
async def del_provider(callback_query: types.CallbackQuery):
    await sqlite_db.sql_del_providers(callback_query.data.replace('pdel ', ''))
    await callback_query.answer(text='Удалена', show_alert=True)


# Регистрация хендлеров
def register_handlers_admin_lk(dp: Dispatcher):
    dp.register_message_handler(command_menu, lambda message: "Main menu" in message.text, state=Providers.all_states)
    dp.register_message_handler(cm_start, state=Providers.type)
    dp.register_message_handler(cm_delete, state=DELproviders.type)
    dp.register_message_handler(load_what, state=Providers.Whatt)
    dp.register_message_handler(load_what_del, state=DELproviders.Whatt)

    dp.register_message_handler(load_where, state=Providers.Wheree)
    dp.register_message_handler(load_comment, state=Providers.Comment)
