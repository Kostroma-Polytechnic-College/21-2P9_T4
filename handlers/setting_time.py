import re

from aiogram import Router, F 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import Form
from data import dbedit
from filters.check_geo import CheckDBField

router = Router()

@router.message((F.text.lower() == "установить время") | (F.text.lower() == "/set_time"),CheckDBField())
async def profile(message: Message, state: FSMContext):
    await state.set_state(Form.time)
    await message.answer("Введите время в которое будет присылаться прогноз погоды. Формат времени - HH:mm")

@router.message(Form.time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time = message.text)
    if isinstance(message.text, str) and re.match(r'(?:[01]\d|2[0-3]):[0-5]\d', message.text):
        await dbedit.edit_time(state, user_id=message.from_user.id)
        await state.clear()
        await message.answer(f"Время отправки прогноза погоды: {message.text}")
    else:
        await message.answer("Введи правильно время")