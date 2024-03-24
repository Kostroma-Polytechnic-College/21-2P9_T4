from aiogram import Router, F
from aiogram.types import CallbackQuery

from logic import weather
from data import dbget

router = Router()

@router.callback_query(lambda c: c.data.isdigit())
async def handle_date(callback_query: CallbackQuery):
    chosen_date = int(callback_query.data)
    forecast_dates = await weather.listDate(chosen_date)
    geo = await dbget.get_geo(callback_query.from_user.id)
    text_weather = await weather.textWeather(geo[0],geo[1],forecast_dates)
    await callback_query.message.delete()
    if chosen_date > 4:
        await callback_query.message.answer(f"Прогноз погоды на {chosen_date} дней \n\n{text_weather}")
    else:
        await callback_query.message.answer(f"Прогноз погоды на {chosen_date} дня \n\n{text_weather}")