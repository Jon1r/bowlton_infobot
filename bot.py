from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import client, admin_providers, other, admin_docs, admin_googledocs, client_sprints, client_tasks


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin_providers.register_handlers_admin_lk(dp)
admin_docs.register_handlers_admin_dc(dp)
admin_googledocs.register_handlers_admin_dc(dp)
client_sprints.register_handlers_client(dp)
client_tasks.register_handlers_client(dp)
#other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
