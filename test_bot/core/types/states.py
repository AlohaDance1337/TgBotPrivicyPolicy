from aiogram.fsm.state import  StatesGroup, State

class DialogPolicy(StatesGroup):
    privacy_policy = State()
    terms_of_use = State()
    create_mail = State()
    name_ = State()
    email = State()
    app_name = State()
    sendUrl = State()

class DialogUse(StatesGroup):
    privacy_use = State()
    terms_of_use = State()
    create_mail = State()
    name = State()
    email = State()
    app_name = State()
    sendUrl = State()

class UpdateStatus_Admin(StatesGroup):
    user_id = State()


class UpdateStatus_Premium(StatesGroup):
    take = State()
    give = State()
