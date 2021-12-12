import sqlite3 as sq
from create_bot import dp, bot
from keyboards import kb_menu

all = None


def sql_start():
    global base, cur
    base = sq.connect('bowlton.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS team(id BIGINT UNIQUE, name TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS providers(types TEXT, whatt TEXT, wheree TEXT, comment TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS followup(type TEXT, chat TEXT, date TEXT, who TEXT, done TEXT, '
                 'todo TEXT, discuss TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS tasks(id TEXT, what TEXT, date DATE)')
    base.execute('CREATE TABLE IF NOT EXISTS YFRfiles(whatt TEXT, wheree TEXT, comment TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS GoogleDocs(whatt TEXT, wheree TEXT, comment TEXT)')
    base.commit()


async def sql_add_team(id, name):
    cur.execute('INSERT INTO team VALUES (?, ?)', (id, name))
    base.commit()


async def sql_add_providers(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO providers VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_del_providers(data):
    cur.execute('DELETE FROM providers WHERE wheree==?', (data,))
    base.commit()


async def sql_add_followup(state):
    async with state.proxy() as data:
        print(1111111111111111111)
        cur.execute('INSERT INTO followup VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_tasks(state):
    async with state.proxy() as data:
        print(1111111111111111111)
        del data['table']
        cur.execute('INSERT INTO tasks VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_yfrfiles(state):
    async with state.proxy() as data:
        print(1111111111111111111)
        cur.execute('INSERT INTO YFRfiles VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_del_yfrfiles(data):
    cur.execute('DELETE FROM YFRfiles WHERE comment==?', (data,))
    base.commit()


async def sql_add_googledocs(state):
    async with state.proxy() as data:
        print(1111111111111111111)
        cur.execute('INSERT INTO GoogleDocs VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_del_googledocs(data):
    print(data)
    cur.execute('DELETE FROM GoogleDocs WHERE whatt==?', (data,))
    base.commit()


async def sql_take_info_providers(message):
    return cur.execute("SELECT * FROM providers WHERE whatt==?", (message,)).fetchall()


async def sql_take_info_yfrfiles(message):
    return cur.execute("SELECT * FROM YFRfiles WHERE whatt==?", (message,)).fetchall()


async def sql_take_info_googledocs(message):
    return cur.execute("SELECT * FROM GoogleDocs WHERE whatt==?", (message,)).fetchall()


async def sql_take_info_tasks(message, id):
    cur.execute("SELECT * FROM tasks WHERE which==?", (message,))
    all = cur.fetchall()
    if all == []:
        await bot.send_message(id, 'Тут пусто', reply_markup=kb_menu)
    else:
        for row in all:
            await bot.send_message(id, row[1] + " - " + row[2], reply_markup=kb_menu)


async def sql_take_info_followup(message, id):
    cur.execute("SELECT * FROM followup WHERE type==?", (message,))
    all = cur.fetchall()
    if all == []:
        await bot.send_message(id, 'Тут пусто', reply_markup=kb_menu)
    else:
        for row in all:
            await bot.send_message(id, row[1] + " - " + row[2], reply_markup=kb_menu)


async def sql_take_info_team():
    cur.execute("SELECT id FROM team")
    all = cur.fetchall()
    return all
