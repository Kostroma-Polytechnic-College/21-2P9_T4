from aiogram import Router, F
from aiogram.types import CallbackQuery

from logic import weather

router = Router()

@router.callback_query(lambda c: c.data.isdigit())
async def handle_date(callback_query: CallbackQuery):
    chosen_date = int(callback_query.data)
    bt = await weather.listDate(chosen_date)
    forecast_dates = bt
    text_weather = await weather.textWeather(forecast_dates)
    await callback_query.message.delete()
    if chosen_date > 4:
        await callback_query.message.answer(f"Прогноз погоды на {chosen_date} дней \n\n{text_weather}")
    else:
        await callback_query.message.answer(f"Прогноз погоды на {chosen_date} дня \n\n{text_weather}")