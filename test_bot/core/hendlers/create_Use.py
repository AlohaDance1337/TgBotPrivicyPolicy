from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery,Message
from core.types.states import DialogUse
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import create_doc
from db.db import Database

import os
import requests

router = Router()

db = Database()

WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://privatizerbot.space')

@router.callback_query(F.data=='create_terms_of_use',)
async def select_TermOfUse(call: CallbackQuery, state: FSMContext):
    await state.set_state(DialogUse.terms_of_use)
    await call.message.answer(text='Введите имя разаботчика:')

@router.message(DialogUse.terms_of_use, F.text)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(dev_username=message.text)
    await message.reply(text='Введите название приложения')
    await state.set_state(DialogUse.app_name)

@router.message(DialogUse.app_name, F.text)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(app_name=message.text)
    await message.reply(text='Введите название email')
    await state.set_state(DialogUse.email)

@router.message(DialogUse.email, F.text)
async def get_message(message: Message, state:FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    email = data["email"]
    dev_username = data["dev_username"]
    app_name = data["app_name"]
    try:
        response = requests.post(
            f'{WEB_APP_URL}/create_document/terms_of_use?dev_username={dev_username}&app_name={app_name}&email={email}')
        try:
                response.raise_for_status()
                response_json = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка: {e}")
            await message.reply(message.from_user.id, "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз.")
            return
        except ValueError as e:
            print(f"Ошибка: {e}")
            await message.reply(message.from_user.id, "Произошла ошибка при обработке ответа сервера. Пожалуйста, попробуйте еще раз.")
            return
    except:
        pass
    document_url = f'{WEB_APP_URL}{response_json["url"]}'
    await message.reply(f"Ваша ссылка на Term Of Use: {document_url}")
    await message.reply("Желаете создать Terms of Use?", reply_markup=create_doc)
    await state.set_state(DialogUse.privacy_use)

@router.callback_query(DialogUse.privacy_use,F.data =="Yes")
async def send_Use(call: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    email = data["email"]
    dev_username = data["dev_username"]
    app_name = data["app_name"]
    try:
        response = requests.post(
            f'{WEB_APP_URL}/create_document/privacy_policy?dev_username={dev_username}&app_name={app_name}&email={email}')
        try:
                response.raise_for_status()
                response_json = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка: {e}")
            await call.message.reply("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз.")
            return
        except ValueError as e:
            print(f"Ошибка: {e}")
            await call.message.reply( "Произошла ошибка при обработке ответа сервера. Пожалуйста, попробуйте еще раз.")
            return
    except:
        pass
    document_url = f'{WEB_APP_URL}{response_json["url"]}'
    db.append_user(name=call.from_user.first_name,username=call.from_user.username, chat_id=call.from_user.id)
    await call.message.answer(f"Ваша ссылка Privacy policy:\n{document_url}")

@router.callback_query(F.data == "No")
async def if_no(call: CallbackQuery):
    await call.message.reply("Принял")