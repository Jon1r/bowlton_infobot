from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

import config
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

#bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)