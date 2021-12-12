from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot

from keyboards import kb_menu, kb_tasks, kb_providers, kb_yfrfiles, kb_parts, kb_followup, kb_produce, kb_hardware, \
    kb_electrica, kb_documents, kb_googledocs
from data_base import sqlite_db

all = None


class Sprints(StatesGroup):
    type = State()
    chat = State()
    date = State()
    who = State()
    done = State()
    todo = State()
    discuss = State()


class Followup(StatesGroup):
    type = State()
    chat = State()
    date = State()
    who = State()
    done = State()
    todo = State()
    discuss = State()


async def command_menu(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Запутался?)', reply_markup=kb_menu)
    await state.finish()


# Включерние режима спринтов
async def command_sprint(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['type'] = 'sprint'
        data['chat'] = '-1001657253379'
        data['date'] = message.date.isocalendar().week
        data['who'] = message.from_user.first_name
    await Sprints.done.set()
    await bot.send_message(message.from_user.id, 'Что было сделано?', reply_markup=types.ReplyKeyboardRemove())


async def command_sprint_done(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['done'] = message.text

    await Sprints.next()
    await bot.send_message(message.from_user.id, 'Что планируешь сделать?')


async def command_sprint_todo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['todo'] = message.text

    await Sprints.next()
    await bot.send_message(message.from_user.id, 'Вопросы на обсуждение')


async def command_sprint_discuss(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['discuss'] = message.text
        await bot.send_message(data['chat'], '#sprint' + data['who'] + ' #week' + str(data['date']) + '\n' + '<b>Сделано:</b>\n' + data['done'] +
                                                                              '\n<b>Буду делать:</b>\n' + data['todo'] +
                                                                              '\n<b>Вопросы на обсуждение:</b>\n' + data['discuss'])

    await bot.send_message(message.from_user.id, 'записал')
    await sqlite_db.sql_add_followup(state)
    await state.finish()


# Включение режима followup
async def command_followup(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['type'] = 'followup'
    await bot.send_message(message.from_user.id, 'Какой сферы касается в большей степени?', reply_markup=kb_followup)
    await Followup.chat.set()


async def command_followup_chat(message: types.Message, state: FSMContext):
    global chat
    if message.text == 'Electronics':
        chat = '-1001657253379'
    elif message.text == 'Software':
        chat = '-1001657253379'
    elif message.text == 'Design':
        chat = '-1001657253379'
    elif message.text == 'Decor':
        chat = '-1001657253379'
    elif message.text == 'Other':
        chat = '-1001657253379'
    async with state.proxy() as data:
        data['chat'] = chat
        data['date'] = message.date
        data['who'] = message.from_user.first_name
    await bot.send_message(message.from_user.id, 'Напиши тему обсуждения обсуждения', reply_markup=types.ReplyKeyboardRemove())
    await Followup.done.set()


async def command_followup_done(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['done'] = message.text
    await bot.send_message(message.from_user.id, 'Что решили по этим вопросам?')
    await Followup.next()


async def command_followup_todo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['todo'] = message.text
    await bot.send_message(message.from_user.id, 'Напиши вопросы требующие дополнительного обсуждения')
    await Followup.next()


async def command_followup_discuss(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['discuss'] = message.text
        await bot.send_message(data['chat'], '#follow_up ' + data['who'] + ' ' + str(data['date']) + '\n' + '<b>Тема:</b>\n' + data['done'] +
                                                                              '\n<b>Принятые решения:</b>\n' + data['todo'] +
                                                                              '\n<b>Вопросы на обсуждение:</b>\n' + data['discuss'])

    await bot.send_message(message.from_user.id, 'Записал')
    await sqlite_db.sql_add_followup(state)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_sprint, lambda message: '/sprint' in message.text, state=None)
    dp.register_message_handler(command_followup, lambda message: "\U0001F4DDFollow-up" in message.text,
                                state=None)
    dp.register_message_handler(command_menu, lambda message: "Main menu" in message.text, state=Sprints.all_states)
    dp.register_message_handler(command_menu, lambda message: "Main menu" in message.text, state=Followup.all_states)
    dp.register_message_handler(command_followup_chat, state=Followup.chat)

    dp.register_message_handler(command_sprint_done, state=Sprints.done)
    dp.register_message_handler(command_sprint_todo, state=Sprints.todo)
    dp.register_message_handler(command_sprint_discuss, state=Sprints.discuss)
    dp.register_message_handler(command_followup_done, state=Followup.done)
    dp.register_message_handler(command_followup_todo, state=Followup.todo)
    dp.register_message_handler(command_followup_discuss, state=Followup.discuss)