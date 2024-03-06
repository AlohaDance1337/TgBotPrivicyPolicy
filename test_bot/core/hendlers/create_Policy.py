from aiogram import Router, F
from aiogram.types import CallbackQuery,Message
from core.types.states import DialogPolicy
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import create_doc
from db.db import Database
from core.filters.filters import PremiumFilter
from core.keyboards.inline import premium_button

import os
import requests

db = Database()

router = Router()

WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://privatizerbot.space')

@router.callback_query(F.data=='create_privacy_policy', PremiumFilter())
async def premium_buttons(call:CallbackQuery):
     await call.message.answer(text="dadsa",reply_markup=premium_button)

@router.callback_query(F.data=='create_privacy_policy')
async def select_PrivacyPolicy(call: CallbackQuery, state: FSMContext):
    await state.set_state(DialogPolicy.privacy_policy)
    await call.message.answer(text='Введите имя разработчика:')

@router.message(DialogPolicy.privacy_policy, F.text)
async def get_message(message: Message, state: FSMContext):
    db.append_user(name=message.from_user.first_name,username=message.from_user.username, chat_id=message.from_user.id)
    await state.update_data(dev_username=[message.text,message.from_user.id])
    await message.reply(text='Введите название приложения:')
    await state.set_state(DialogPolicy.app_name)

@router.message(DialogPolicy.app_name, F.text)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(app_name=message.text)
    await message.reply(text='Введите название email:')
    await state.set_state(DialogPolicy.email)

@router.message(DialogPolicy.email, F.text)
async def get_message(message: Message, state:FSMContext):
    await state.update_data(email=message.text, user_id=message.from_user.id)
    data = await state.get_data()
    email = data["email"]
    dev_username = data["dev_username"][0]
    app_name = data["app_name"]
    chat_id=data["dev_username"][1]
    try:
        response = requests.post(
            f'{WEB_APP_URL}/create_document/privacy_policy?dev_username={dev_username}&app_name={app_name}&email={email}&user_id={chat_id}')
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
    await message.reply(f"Ваша ссылка на Privicy policy: {document_url}")
    await message.reply("Желаете создать Terms of Use?", reply_markup=create_doc)
    await state.set_state(DialogPolicy.terms_of_use)

@router.callback_query(DialogPolicy.terms_of_use,F.data =="Yes")
async def send_Use(call: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    email = data["email"]
    dev_username = data["dev_username"]
    app_name = data["app_name"]
    chat_id=data["dev_username"][1]
    try:
        response = requests.post(
            f'{WEB_APP_URL}/create_document/terms_of_use?dev_username={dev_username}&app_name={app_name}&email={email}&user_id={chat_id}')
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
    await call.message.answer(f"Ваша ссылка Term of Use:\n{document_url}")

@router.callback_query(F.data == "No")
async def if_no(call: CallbackQuery):
    await call.message.reply("Принял")
