from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery,Message
from core.types.states import Dialog
from aiogram.fsm.context import FSMContext

router = Router()

# @router.callback_query(F.data=='')
# async def select_PrivacyPolicy(call: CallbackQuery, bot: Bot, state: FSMContext):
#     await state.set_state(Dialog.privacy_policy)
#     await call.message.answer(text='Введите имя разаботчика:')

# @router.message(Dialog.privacy_policy, F.text)
# async def get_message(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.reply(text='Введите название приложения')
#     await state.set_state(Dialog.app_name)

# @router.message(Dialog.app_name, F.text)
# async def get_message(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.reply(text='Введите название email')
#     await state.set_state(Dialog.email)

# @router.message(Dialog.email, F.text)
# async def get_message(message: Message, state:FSMContext):
#     await state.update_data(name=message.text)