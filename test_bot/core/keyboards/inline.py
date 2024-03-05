from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
select_Button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Создать Privacy Policy",
            callback_data = "create_privacy_policy", 
        )

    ],
    [
        InlineKeyboardButton(
            text = "Создать Terms of Use", 
            callback_data = "create_terms_of_use"
            )
    ]
]
)

premium_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = "Собирать данные",
            callback_data="collect_data"
        )
    ],
    [
        InlineKeyboardButton(
            text="Не собирать данные",
            callback_data="dont_collect_data"
        )
    ]
])

create_doc = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Да",
            callback_data = "Yes"
    )],
    [
        InlineKeyboardButton(
            text="Нет",
            callback_data = "No"
        )
    ]

])
admin_buttons = InlineKeyboardMarkup(inline_keyboard=
[
    [
        InlineKeyboardButton(
            text="Рассылка",
            callback_data="mailing"
        )
    ],
    [
        InlineKeyboardButton(
            text="Выдать премиум",
            callback_data="give_premium"
        )
    ],
    [
        InlineKeyboardButton(
            text="Забрать премиум",
            callback_data="take_away_premium"
        )
    ],
    [
        InlineKeyboardButton(
            text="Статистика",
            callback_data="statistics"
        )
    ],
    [
        InlineKeyboardButton(
            text = "Статистика за последние 10 человек",
            callback_data="statistics_for_10"
        )
    ]
])

doc_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Privacy Policy",
            callback_data="privacy_policy"
        )
    ],
    [
        InlineKeyboardButton(
            text="Terms of Use",
            callback_data="term_of_use"
        )
    ]
])

creator_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Выдать админ",
            callback_data="give_admin"
        )
    ],
    [
        InlineKeyboardButton(
            text="Забрать админ",
            callback_data="take_away_admin"
        )
    ]
])