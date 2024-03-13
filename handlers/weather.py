import asyncio
import requests
import json

from aiogram import Bot
from config_reader import config
from datetime import datetime
from data import database

async def send_weather(bot: Bot, nearest_time):
    lsUsers = await database.get_listUsers(nearest_time)
    textWr = await textWeather()
    for user_id in lsUsers:
        await bot.send_message(chat_id=f"{user_id[0]}",text=textWr)

async def scheduler(bot: Bot):
    while True:
        currentTime = datetime.now().strftime("%H:%M")
        nearestTime = await database.get_nearestTime()
        if nearestTime == currentTime:
            await send_weather(bot, currentTime)
        await asyncio.sleep(60)

async def get_weather():
    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast?lat=57.76791&lon=40.926894&[lang=ru_RU]'
    yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': config.yandex_api.get_secret_value()})
    data = json.loads(yandex_req.text)
    temp = data['fact']['temp']
    humidity = data['fact']['humidity']
    feels_like = data['fact']['feels_like']
    wind_speed = data['fact']['wind_speed']
    condition = data['fact']['condition']
    pressure_mm = data['fact']['pressure_mm']
    current_condition = conditions.get(condition)

    return temp,humidity,feels_like,wind_speed,pressure_mm,current_condition

async def textWeather():
    temp, humidity, feels_like, wind_speed, pressure_mm, current_condition = await get_weather()
    return (f"Погода в Костроме \nТемпература: {temp}°C (ощущается как {feels_like}°C) \nСкорость ветра: {wind_speed} м/c\nВлажность: {humidity}%" 
    f"\nДавление: {pressure_mm} (в мм рт.ст.)\nСостояние погоды: {current_condition}")
