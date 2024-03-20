from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Установить время"),
            KeyboardButton(text = "Получить текущую погоду"),
            KeyboardButton(text = "Отменить рассылку")
        ]
    ],
    resize_keyboard= True,
    input_field_placeholder="Выберите действие из меню"
) 