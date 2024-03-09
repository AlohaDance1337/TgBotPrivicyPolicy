from aiogram.types import Message, CallbackQuery
from aiogram import Bot,Router,F
from core.keyboards.inline import admin_buttons
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from core.keyboards.inline import creator_buttons
from db.db import Database
from core.filters.filters import CreatorFilter
from core.types.states import UpdateStatus_Admin

router = Router()

db = Database()

@router.message(F.text,CreatorFilter(),Command('creator'))
async def admin_button(message:Message):
    await message.answer(text="Вы вызвали чёто-там", reply_markup=creator_buttons)

@router.callback_query(F.data == "give_admin")
async def get_username(call:CallbackQuery, state:FSMContext):
    await call.message.reply("Введите id пользователя:")
    await state.set_state(UpdateStatus_Admin.give)

@router.message(UpdateStatus_Admin.give,F.text)
async def give_admin(message:Message, bot:Bot, state:FSMContext):
    db.give_status_admin(int(message.text))
    await message.reply("Был выдан статус админ")
    await bot.send_message(chat_id= int(message.text), text="Вам был выдан статус админ")
    await state.clear()

@router.callback_query(F.data == "take_away_admin")
async def get_username(call:CallbackQuery, state:FSMContext):
    await call.message.reply("Введите id пользователя:")
    await state.set_state(UpdateStatus_Admin.take)

@router.message(UpdateStatus_Admin.take)
async def give_admin(message:Message, bot:Bot,state:FSMContext):
    db.take_away_status(int(message.text),"take_away_admin")
    await message.reply("Был забран статус админа")
    await bot.send_message(chat_id= int(message.text), text="Вам убрали статус админ")
    await state.clear()