from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from core.filters.filters import PremiumFilter
from db.db import Database
from aiogram.types import CallbackQuery
from core.types.states import DialogUsePremium,DialogPolicyPremium
from aiogram.types import Message
from core.keyboards.inline import create_doc, doc_buttons

import requests

db = Database()

router = Router()

WEB_APP_URL = 'http://192.168.0.101:8000'

@router.callback_query(F.data == "collect_data",PremiumFilter())
async def premium_buttons(call:CallbackQuery,state:FSMContext):
    await state.set_state(DialogUsePremium.terms_of_use)
    await call.message.answer(text='Введите имя разаботчика:')

@router.message(DialogUsePremium.terms_of_use, F.text)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(dev_username=[message.text,message.from_user.id])
    await message.reply(text='Введите название приложения')
    await state.set_state(DialogUsePremium.app_name)

@router.message(DialogUsePremium.app_name, F.text)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(app_name=message.text)
    await message.reply(text='Введите название email')
    await state.set_state(DialogUsePremium.email)

@router.message(DialogUsePremium.email, F.text)
async def get_message(message: Message, state:FSMContext):
    await state.update_data(email=message.text)
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
    await state.set_state(DialogUsePremium.privacy_use)

@router.callback_query(DialogUsePremium.privacy_use,F.data =="Yes")
async def send_Use(call: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    email = data["email"]
    dev_username = data["dev_username"][0]
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
    db.append_user(name=call.from_user.first_name,username=call.from_user.username, chat_id=call.from_user.id)
    await call.message.answer(f"Ваша ссылка Terms of Use:\n{document_url}")

