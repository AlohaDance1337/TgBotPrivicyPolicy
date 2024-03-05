from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message,CallbackQuery
from db.db import Database

db = Database()

class PremiumFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        return db.get_status(call.from_user.id)[0][0]==1
    
class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return db.get_status(message.from_user.id)[0][1]==1
    
class CreatorFilter(BaseFilter):
    async def __call__(self, message:Message) -> bool:
        return db.get_status(message.from_user.id)[0][2]==1