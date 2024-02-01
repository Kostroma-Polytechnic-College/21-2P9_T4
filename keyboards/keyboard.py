from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Установка времени"),
        ]
    ],
    resize_keyboard= True,
    input_field_placeholder="Выберите действие из меню"
) 