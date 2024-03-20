from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import keyboard
from handlers import weather
from data import database

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать",reply_markup=keyboard.main_kb)

@router.message((F.text.lower() == "получить текущую погоду") | (F.text.lower() == "/get_weather"))
async def currentWeather(message: Message):
    textWeather = await weather.textWeather()
    await message.answer(textWeather)

@router.message((F.text.lower() == "отменить рассылку") | (F.text.lower() == "/delete_mailing"))
async def cansel_mailing(message: Message):
    deleteuser = await database.delete_user(message.from_user.id)
    if deleteuser == True:
        await message.answer("Рассылка отменена")
    else:
        await message.answer("У вас не была включена рассылка")