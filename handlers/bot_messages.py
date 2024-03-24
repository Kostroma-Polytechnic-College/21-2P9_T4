from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.types import ContentType

from keyboards import reply, inline
from logic import weather
from data import dbdelete, dbget, database, dbedit
from filters.check_geo import CheckDBField

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать",reply_markup=reply.rep_kb)

@router.message((F.text.lower() == "получить текущую погоду") | (F.text.lower() == "/get_weather"), CheckDBField())
async def currentWeather(message: Message):
    geo = await dbget.get_geo(message.from_user.id)
    textWeather = await weather.textWeather(geo[0],geo[1])
    await message.answer(textWeather)

@router.message((F.text.lower() == "отменить рассылку") | (F.text.lower() == "/delete_mailing"))
async def cansel_mailing(message: Message):
    deleteuser = await dbdelete.delete_time(message.from_user.id)
    if deleteuser == True:
        await message.answer("Рассылка отменена")
    else:
        await message.answer("У вас не была включена рассылка")

@router.message((F.text.lower() == "получить будущую погоду") | (F.text.lower() == "/get_weatherForecast"), CheckDBField())
async def featureWeather(message: Message):
    await message.answer("Выберите дату для получения прогноза погоды", reply_markup=inline.inl_kb)

@router.message((F.text.lower() == "установить геопозицию") | (F.text.lower() == "/set_geo"))
async def featureWeather(message: Message):
    await message.answer("Для продолжения отправьте свою геопозицию", reply_markup=reply.spec_kb)

@router.message((F.text.lower() == "назад"))
async def featureWeather(message: Message):
    await message.answer(text="Возврат в начальное меню",reply_markup=reply.rep_kb)

@router.message(F.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    profile_exists = await dbget.get_user(user_id=message.from_user.id)
    if profile_exists == "не указан":
        await database.create_profile(user_id=message.from_user.id)
    await dbedit.edit_geo(message.from_user.id, latitude, longitude)
    await message.answer(f"Ваша геопозиция: {latitude}, {longitude}")