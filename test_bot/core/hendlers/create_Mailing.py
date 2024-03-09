from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery,Message
from aiogram.fsm.context import FSMContext
from core.filters.filters import AdminFilter
from core.types.states import StateMailing
from db.db import Database


router = Router()

db = Database()

@router.callback_query(F.data=="mailing")
async def mailing(call:CallbackQuery,state:FSMContext):
    await state.set_state(StateMailing.mailing)
    await call.message.answer("Ведите текст сообщения:")

@router.message(F.text,StateMailing.mailing)
async def mailing_message(message:Message,bot:Bot):
    count = 0
    for user_id in db.get_users_chats_id():
        if db.get_status(user_id)[0][2]!=1 and db.get_status(user_id)[0][1]!=1:
            await bot.send_message(chat_id=int(user_id), text= message.text)
            count+=1
    await message.reply(f"Рассылка была завершена.\nВсего сообщений отправлено: {1}")    