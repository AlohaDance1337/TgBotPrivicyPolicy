import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.hendlers import create_Policy,create_Use,cmd_admin,premium_buttons
from aiogram import Router
from core.hendlers.basic import get_inline
from dotenv import load_dotenv
from db.db import Database


load_dotenv()

API_TOKEN = os.getenv('token_bot')
WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://privatizerbot.space')

logging.basicConfig(level=logging.INFO,filename="logsMain",filemode='w')

bot = Bot(token=API_TOKEN)

db = Database()

dp = Dispatcher()
dp.include_routers(cmd_admin.router, create_Policy.router, create_Use.router, premium_buttons.router)

admin_id = 1107806304
           
router = Router()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__': 
    dp.message.register(get_inline, Command(commands='start'))
    
    asyncio.run(main())