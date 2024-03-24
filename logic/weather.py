import requests
import json

from datetime import datetime,timedelta
from config_reader import config
from datetime import datetime

async def connect_yandex(latitude,longitude):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': config.yandex_api.get_secret_value()})
    data = json.loads(yandex_req.text)
    return data

async def get_weather(latitude,longitude):
    data = await connect_yandex(latitude,longitude)

    temp = data['fact']['temp']
    humidity = data['fact']['humidity']
    feels_like = data['fact']['feels_like']
    wind_speed = data['fact']['wind_speed']
    condition = data['fact']['condition']
    pressure_mm = data['fact']['pressure_mm']
    current_condition = conditions.get(condition)

    return {
        'date': (datetime.now()).strftime('%Y-%m-%d'),
        'temp': temp,
        'humidity': humidity,
        'feels_like': feels_like,
        'wind_speed': wind_speed,
        'pressure_mm': pressure_mm,
        'condition': current_condition
    }

async def get_weatherForecast(latitude,longitude,forecast_dates):
    data = await connect_yandex(latitude,longitude)
    
    forecasts = []
    for forecast_date in forecast_dates:
        forecast = next(filter(lambda x: x['date'] == forecast_date, data['forecasts']), None)
        if forecast:
            day_short_forecast = forecast['parts']['day']
            temp = day_short_forecast['temp_avg']
            humidity = day_short_forecast['humidity']
            feels_like = day_short_forecast['feels_like']
            wind_speed = day_short_forecast['wind_speed']
            condition = day_short_forecast['condition']
            pressure_mm = day_short_forecast['pressure_mm']
            current_condition = conditions.get(condition)
            forecasts.append({
                'date': forecast_date,
                'temp': temp,
                'humidity': humidity,
                'feels_like': feels_like,
                'wind_speed': wind_speed,
                'pressure_mm': pressure_mm,
                'condition': current_condition
            })
    
    return forecasts

async def textWeather(latitude,longitude,forecast_dates=None):
    if forecast_dates:
        forecasts = await get_weatherForecast(latitude,longitude, forecast_dates)
    else:
        forecasts = [await get_weather(latitude,longitude)]

    weather_message = "Прогноз погоды в вашей геопозиции:\n\n"
    for forecast in forecasts:
        weather_message += f"Дата: {forecast['date']}\n"
        weather_message += f"Температура: {forecast['temp']}°C (ощущается как {forecast['feels_like']}°C)\n"
        weather_message += f"Скорость ветра: {forecast['wind_speed']} м/c\n"
        weather_message += f"Влажность: {forecast['humidity']}%\n"
        weather_message += f"Давление: {forecast['pressure_mm']} (в мм рт.ст.)\n"
        weather_message += f"Состояние погоды: {forecast['condition']}\n\n"
    return weather_message

async def listDate(dat):
    start_date = datetime.now()
    buttons = []
    for i in range(dat):
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')
        buttons.append(formatted_date)
    return buttons
    

conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
             }