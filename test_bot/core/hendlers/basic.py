from aiogram.types import Message
from aiogram import Bot
from core.keyboards.inline import select_Button

async def get_inline(message: Message, bot: Bot):
    await message.answer(text='Продолжите фразу: Сегодня я хочу...',
                        reply_markup= select_Button)