import os

import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем свой API ключ Яндекс.Погоды
YANDEX_WEATHER_API_KEY = os.getenv('YANDEX_WEATHER_API_KEY')


async def get_weather_data(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    if not location:
        return f"Город '{city}' не найден."

    lat, lon = location.latitude, location.longitude
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU"
    headers = {"X-Yandex-API-Key": YANDEX_WEATHER_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        fact = data["fact"]
        weather_condition = fact["condition"]
        temperature = fact["temp"]
        feels_like = fact["feels_like"]
        return f"Погода в городе {city}: {weather_condition}, Температура: {temperature}°C, Ощущается как: {feels_like}°C"
    else:
        return f"Не удалось получить данные о погоде для города {city}. Код ошибки: {response.status_code}"
