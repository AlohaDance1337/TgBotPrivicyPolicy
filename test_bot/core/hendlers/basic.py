from aiogram.types import Message
from aiogram import Bot
from core.keyboards.inline import select_Button
from db.db import Database

db = Database()

async def get_inline(message: Message, bot: Bot):
    await message.answer(text='Продолжите фразу: Сегодня я хочу...',
                        reply_markup= select_Button)
    db.append_user(name=message.from_user.first_name,username=message.from_user.username, chat_id=message.from_user.id)