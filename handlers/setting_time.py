import re

from aiogram import Router, F 
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Form
from data import database

router = Router()

@router.message((F.text.lower() == "установка времени") | (F.text.lower() == "/set_time"))
async def profile(message: Message, state: FSMContext):
    await state.set_state(Form.time)
    await message.answer("Введите время в которое будет присылаться прогноз погоды. Формат времени - HH:mm")
    await database.create_profile(user_id= message.from_user.id)

@router.message(Form.time)
async def profile(message: Message, state: FSMContext):
    await state.update_data(time = message.text)
    if re.match(r'[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}', message.text):
        await database.edit_profile(state, user_id=message.from_user.id)
        await state.clear()
        await message.answer(f"Время отправки прогноза погоды: {message.text}")
    else:
        await message.answer("Введи правильно время")