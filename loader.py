from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.books import BooksDB
from utils.db_api.main import Database
from utils.db_api.students import StudentsDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
bks = BooksDB(db)
stdb = StudentsDB(db)
