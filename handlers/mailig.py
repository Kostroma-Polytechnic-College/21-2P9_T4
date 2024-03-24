import asyncio

from datetime import datetime
from aiogram import Bot
from datetime import datetime
from data import dbget
from logic import weather

async def send_weather(bot: Bot, nearest_time):
    lsUsers = await dbget.get_listUsers(nearest_time)
    for user_id in lsUsers:
        geo = await dbget.get_geo(user_id[0])
        textWr = await weather.textWeather(geo[0], geo[1])
        await bot.send_message(chat_id=f"{user_id[0]}",text=textWr)

async def scheduler(bot: Bot):
    while True:
        currentTime = datetime.now().strftime("%H:%M")
        nearestTime = await dbget.get_nearestTime()
        if nearestTime == currentTime:
            await send_weather(bot, currentTime)
        await asyncio.sleep(60)
