from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from keyboards import kb_menu, kb_tasks, kb_providers, kb_yfrfiles, kb_parts, kb_followup, kb_produce, kb_hardware, \
    kb_electrica, kb_documents, kb_googledocs
from data_base import sqlite_db

all = None


class FSMClient(StatesGroup):
    name = State()
    providers = State()
    questions = State()
    tasks = State()
    yfrfiles = State()
    googledocs = State()


# Стартовая страница СДЕЛАТЬ ИДЕНТИФИКАЦИЮ
async def command_start(message: types.Message):
    print(message.date)
    all = await sqlite_db.sql_take_info_team()
    if message.from_user.id in all[0]:

        try:
            await bot.send_message(message.from_user.id, 'Привет ' + message.from_user.first_name + '!\n' + 'Чем я могу быть полезен?',
                                       reply_markup=kb_menu)

        except:
            await message.reply('All questions u can ask in privat message')

    else:

        try:
            await bot.send_message(message.from_user.id, 'Привет ' + message.from_user.first_name + '!',
                                   reply_markup=kb_menu)
            await sqlite_db.sql_add_team(message.from_user.id, message.from_user.first_name)

        except:
            await message.reply('All questions u can ask in privat message')
    await message.delete()


async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, <b>пользователь</b>!\n '
                                                 '\nЯ помогу тебе с поиском любой информации.\n'
                                                 'Questions - Здесь ты можешь задать любой интересующий вопрос и указать срочность его решения.\n'
                                                 '\nTasks - Здесь ты сможешь посмотреть свои задачи на спринт, поставить задачу другому человеку, а так же посмотреть глобальный сценарий, к которому нужно стремиться.\n'
                                                 '\nProviders - Здесь ты сможешь найти поставщиков по всем закупкам и услугам, которыми мы пользовались ранее.\n'
                                                 '\nYFRfiles - Здесь вы найдете различные файлы связанные с фирмой: доверенность, реквизиты, ссылки на все гугл диски.', reply_markup=kb_menu)
    await message.delete()


async def command_admin(message: types.Message):
    await bot.send_message(message.from_user.id, '/add_providers - Этой командой ты можешь добавить сайт поставщика\n'
                                                 '/add_googledoc - Этой командой ты можешь загрузить нужный документ \n'
                                                 '/add_file - Этой командой ты можешь добавить любой документ\n'
                                                 '/del_providers - Этой командой вы можете удалить сайт неактуального поставщика\n'
                                                 '/del_googledoc - Этой командой ты можешь удалить гугл ссылку\n'
                                                 '/del_file - Этой командой ты можешь удалить ненужный файл', reply_markup=kb_menu)
    await message.delete()


async def command_add_name(message: types.Message, state: FSMContext):
    await sqlite_db.sql_add_team(message.from_user.id, message)
    await state.finish()


# Возвращение в главное меню
async def command_menu(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Запутался?)', reply_markup=kb_menu)
    await state.finish()


async def command_menu_1(message: types.Message):
    await bot.send_message(message.from_user.id, 'Запутался?)', reply_markup=kb_menu)


# Разделы главного меню
async def command_followup(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери напраления разговора для отправки резюме встречи', reply_markup=kb_followup)
    await FSMClient.questions.set()


async def command_yfrfiles(message: types.Message):
    await bot.send_message(message.from_user.id, 'Какие файлы тебе нужны?', reply_markup=kb_yfrfiles)


async def command_tasks(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Можешь посмотреть свои задачи или узнать ближайшую цель всей команды!',
                           reply_markup=kb_tasks)


async def command_providers(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери, что ты ищешь?', reply_markup=kb_providers)


# Раздел Providers->
async def command_parts(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Что именно интересует?', reply_markup=kb_parts)
    await FSMClient.providers.set()


async def command_hardware(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Что именно интересует?', reply_markup=kb_hardware)
    await FSMClient.providers.set()


async def command_electrica(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Что именно интересует?', reply_markup=kb_electrica)
    await FSMClient.providers.set()


async def command_produced(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Что именно интересует?', reply_markup=kb_produce)
    await FSMClient.providers.set()


# Раздел YFRfiles->
async def command_documents(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Какой нужен документ?', reply_markup=kb_documents)
    await FSMClient.yfrfiles.set()


async def command_googledocs(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Какой нужен документ?', reply_markup=kb_googledocs)
    await FSMClient.googledocs.set()


# Передача инфы для поиска в нужной БД
async def command_info_providers(message: types.Message, state: FSMContext):
    all = await sqlite_db.sql_take_info_providers(message.text.lower())
    if all == []:
        await bot.send_message(message.from_user.id, 'Тут пусто', reply_markup=kb_menu)
    else:
        for row in all:
            await bot.send_message(message.from_user.id, row[2] + " - " + row[3], reply_markup=kb_menu)
    await state.finish()


async def command_info_tasks(message: types.Message, state: FSMContext):
    await sqlite_db.sql_take_info_tasks(message.text.lower(), message.from_user.id)
    await state.finish()


# Раздел Questions->выбор чата
# Раздел YFRfiles->Documents
async def command_info_yfrfiles(message: types.Message, state: FSMContext):
    all = await sqlite_db.sql_take_info_yfrfiles(message.text.lower())
    if all == []:
        await bot.send_message(message.from_user.id, 'Тут пусто', reply_markup=kb_menu)
    else:
        for row in all:
            await bot.send_document(message.from_user.id, row[1], reply_markup=kb_menu)
    await state.finish()


# Раздел YFRfiles->GoogleDocs
async def command_info_googledocs(message: types.Message, state: FSMContext):
    all = await sqlite_db.sql_take_info_googledocs(message.text.lower())
    if all == []:
        await bot.send_message(message.from_user.id, 'Тут пусто', reply_markup=kb_menu)
    else:
        for row in all:
            await bot.send_message(message.from_user.id, row[1] + " - " + row[2], reply_markup=kb_menu)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_message_handler(command_help, commands=['help'], state=None)
    dp.register_message_handler(command_admin, commands=['admin'], state=None)
    dp.register_message_handler(command_menu, lambda message: "Main menu" in message.text, state=FSMClient.all_states)
    dp.register_message_handler(command_menu_1, lambda message: "Main menu" in message.text, state=None)

    dp.register_message_handler(command_tasks, lambda message: "\U0001F3AFTasks" in message.text, state=None)
    dp.register_message_handler(command_providers, lambda message: "\U0001F6D2Providers" in message.text, state=None)
    dp.register_message_handler(command_yfrfiles, lambda message: "\U0001F4C1YRFfiles" in message.text, state=None)

    dp.register_message_handler(command_parts, lambda message: "Parts" in message.text, state=None)
    dp.register_message_handler(command_hardware, lambda message: "Hardware" in message.text, state=None)
    dp.register_message_handler(command_electrica, lambda message: "Electrica" in message.text, state=None)
    dp.register_message_handler(command_produced, lambda message: "Produces" in message.text, state=None)

    dp.register_message_handler(command_documents, lambda message: "Documents" in message.text, state=None)
    dp.register_message_handler(command_googledocs, lambda message: "GoogleDocs" in message.text, state=None)

    dp.register_message_handler(command_info_providers, state=FSMClient.providers)
    dp.register_message_handler(command_info_tasks, state=FSMClient.tasks)
    dp.register_message_handler(command_info_yfrfiles, state=FSMClient.yfrfiles)
    dp.register_message_handler(command_info_googledocs, state=FSMClient.googledocs)
    dp.register_message_handler(command_add_name, state=FSMClient.name)
