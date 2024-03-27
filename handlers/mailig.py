import asyncio

from datetime import datetime
from aiogram import Bot
from datetime import datetime
from data import database
from logic import weather

async def send_weather(bot: Bot, nearest_time):
    lsUsers = await database.get_listUsers(nearest_time)
    textWr = await weather.textWeather()
    for user_id in lsUsers:
        await bot.send_message(chat_id=f"{user_id[0]}",text=textWr)

async def scheduler(bot: Bot):
    while True:
        currentTime = datetime.now().strftime("%H:%M")
        nearestTime = await database.get_nearestTime()
        if nearestTime == currentTime:
            await send_weather(bot, currentTime)
        await asyncio.sleep(60)
