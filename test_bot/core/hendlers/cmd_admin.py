from aiogram.types import Message, CallbackQuery
from aiogram import Bot,Router,F
from core.keyboards.inline import admin_buttons
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from core.keyboards.inline import admin_buttons
from db.db import Database
from core.filters.filters import AdminFilter
from core.types.states import UpdateStatus_Premium

router = Router()

db = Database()


@router.message(AdminFilter(),(F.text.lower() == "admin")|(F.text.lower() == "/admin"))
async def admin_button(message:Message):
    await message.answer(text="Вы вызвали чёто-там", reply_markup=admin_buttons)

@router.callback_query(F.data == "give_premium")
async def get_username(call:CallbackQuery, state:FSMContext):
    await call.message.reply("Введите id пользователя:")
    await state.set_state(UpdateStatus_Premium.give)

@router.message(UpdateStatus_Premium.give,F.text)
async def give_premium(message:Message, bot:Bot):
    db.give_status_premium(int(message.text))
    await message.reply("Был выдан премиум статус")
    await bot.send_message(chat_id= int(message.text), text="Вам был выдан премиум статус")

@router.callback_query(F.data == "statistics")
async def get_statistics(call:CallbackQuery):
    await call.message.answer(text=f"В боте зарегистрированны {len(db.get_statistics())} человек")

@router.callback_query(F.data == "take_away_premium")
async def get_username(call:CallbackQuery, state:FSMContext):
    await call.message.reply("Введите id пользователя:")
    await state.set_state(UpdateStatus_Premium.take)

@router.message(UpdateStatus_Premium.take)
async def give_premium(message:Message, bot:Bot):
    db.take_away_status(int(message.text),"take_away_premium")
    await message.reply("Был забран премиум статус")
    await bot.send_message(chat_id= int(message.text), text="Вам убрали премиум статус")

@router.callback_query(F.data == "statistics_for_10")
async def statistics_for_10(call:CallbackQuery):
    await call.message.answer(text = f'Последние пользователи, которые зарегистрировали:{",".join(db.get_last_10())}')