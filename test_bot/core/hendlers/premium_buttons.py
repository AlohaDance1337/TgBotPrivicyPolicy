from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from core.filters.filters import PremiumFilter
from db.db import Database
from aiogram.types import CallbackQuery

import requests

db = Database()

router = Router()

@router.callback_query(F.data == "collect_data",PremiumFilter())
async def premium_buttons(call:CallbackQuery):
    document_url = ""
    await call.message.answer(f"Ваша ссылка на документ:{document_url}")    #вставте сюда ссылку на создание документа, 
                                                                            #при статусе премиум, как в хэндлере create_Use и create_Policy

@router.callback_query(F.data == "dont_collect_data",PremiumFilter())
async def premium_buttons(call:CallbackQuery):
    await call.message.reply("Принял")