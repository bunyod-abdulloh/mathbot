from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from data.config import REDIS_PASS
from utils.db_api.books import BooksDB
from utils.db_api.main_db import Database
from utils.db_api.students import StudentsDB
from utils.db_api.users_admins import UsersAdminsDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host='localhost', port=6379, password=REDIS_PASS, state_ttl=3000, data_ttl=3000)
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersAdminsDB(db)
bks = BooksDB(db)
stdb = StudentsDB(db)
