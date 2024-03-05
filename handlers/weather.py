import asyncio
from aiogram import Bot
import aioschedule
import sqlite3 as sq
import requests
import json
from config_reader import config

created_tasks = {}

async def noon_print(bot: Bot, chat_id):
    temp, humidity, feels_like, wind_speed, pressure_mm, current_condition = await get_weather()
    await bot.send_message(chat_id=f"{chat_id}",text=f"Погода в Костроме \nТемпература: {temp}°C (ощущается как {feels_like}°C) \nСкорость ветра: {wind_speed} м/c\nВлажность: {humidity}%  \nДавление: {pressure_mm} (в мм рт.ст.)\nСостояние погоды: {current_condition}")

async def scheduler(bot: Bot):
    db = sq.connect("tg.db")
    cur = db.cursor()
    while True:
        cur.execute("SELECT * FROM profile")
        for time_value in cur.fetchall():
            chat_id = time_value[0]
            time = time_value[1]
            if chat_id in created_tasks:
                if created_tasks[chat_id]["time"] != time:
                    aioschedule.cancel_job(created_tasks[chat_id]["job"])
                    del created_tasks[chat_id]
            elif (chat_id, time) not in created_tasks:
                job = aioschedule.every().day.at(time_value[1]).do(noon_print, bot, chat_id)
                created_tasks[chat_id] = {"job": job, "time": time}
        await aioschedule.run_pending()
        await asyncio.sleep(5)


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