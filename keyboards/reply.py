from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rep_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Установить время"),
            KeyboardButton(text = "Получить текущую погоду"),
        ],
        [
            KeyboardButton(text = "Отменить рассылку"),
            KeyboardButton(text = "Получить будущую погоду")
        ],
        [
            KeyboardButton(text = "Установить геопозицию")
        ]
    ],
    resize_keyboard= True,
    input_field_placeholder="Выберите действие из меню"
) 

spec_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Отправить геопозицию", request_location=True),
            KeyboardButton(text = "Назад")
        ]
    ],
    resize_keyboard= True,
    input_field_placeholder="Выберите действие из меню"
)