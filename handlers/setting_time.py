import re

from aiogram import Router, F 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import Form
from data import database

router = Router()

@router.message((F.text.lower() == "установить время") | (F.text.lower() == "/set_time"))
async def profile(message: Message, state: FSMContext):
    await state.set_state(Form.time)
    await message.answer("Введите время в которое будет присылаться прогноз погоды. Формат времени - HH:mm")
    profile_exists = await database.get_user(user_id=message.from_user.id)
    if profile_exists == "не указан":
        await database.create_profile(user_id=message.from_user.id , time="07:00")

@router.message(Form.time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time = message.text)
    if isinstance(message.text, str) and re.match(r'(?:[01]\d|2[0-3]):[0-5]\d', message.text):
        await database.edit_profile(state, user_id=message.from_user.id)
        await state.clear()
        await message.answer(f"Время отправки прогноза погоды: {message.text}")
    else:
        await message.answer("Введи правильно время")