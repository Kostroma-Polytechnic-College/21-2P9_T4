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
        ]
    ],
    resize_keyboard= True,
    input_field_placeholder="Выберите действие из меню"
) 