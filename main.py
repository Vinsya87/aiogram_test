import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv

from cache import is_cache_valid, update_cache, weather_cache
from database import WeatherDatabase
from weather import get_weather_data
from weather_generator import generate_weather_data

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# Список доступных городов
AVAILABLE_CITIES = ['Москва', 'Санкт-Петербург', 'Новосибирск']


# Время жизни кэша в секундах (10 минут)
CACHE_TTL = 600

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Введите ваш город:")


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Доступные команды:\n"
                        "/start - Начать взаимодействие с ботом\n"
                        "/help - Показать список команд\n"
                        "/cities - Вывести список доступных городов\n"
                        "/weather_data - Проверить данные в БД\n"
                        "/random - Произвольная погода2")


# Обработчик команды /random
@dp.message_handler(commands=['random'])
async def random_command(message: types.Message):
    temperature, wind_speed, wind_direction, precipitation = generate_weather_data()

    response = f"Случайная погода:\n" \
               f"Температура: {temperature}°C\n" \
               f"Скорость ветра: {wind_speed} м/c\n" \
               f"Направление ветра: {wind_direction}\n" \
               f"Осадки: {precipitation}"

    await message.answer(response)


# Обработчик команды /cities
@dp.message_handler(commands=['cities'])
async def cities_command(message: types.Message):
    cities_list = "\n".join([f"{i + 1}. {city.title()}" for i, city in enumerate(AVAILABLE_CITIES)])
    await message.reply(f"Список доступных городов:\n{cities_list}")

weather_db = WeatherDatabase()


# Обработчик команды /weather_data
@dp.message_handler(commands=['weather_data'])
async def weather_data_command(message: types.Message):
    # Создаем экземпляр класса WeatherDatabase
    try:
        await weather_db.connect()
        rows = await weather_db.get_weather_data_from_db()
        if not rows:
            await message.answer("В базе данных нет данных о погоде.")
        else:
            response = "Данные о погоде в базе данных:\n"
            for row in rows:
                response += f"ID: {row['id']}, Город: {row['city']}, Погода: {row['weather_data']}, Время: {row['created_at']}\n"
            await message.answer(response)
    finally:
        # Закрываем соединение с базой данных
        await weather_db.disconnect()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    city = message.text.strip().lower()

    if city in map(str.lower, AVAILABLE_CITIES):
        # Есть ли данные о погоде для данного города в кэше и актуальны ли они
        if is_cache_valid(city, CACHE_TTL):
            weather_data = weather_cache[city]['data']
        else:
            # Если данные не в кэше или устарели, делаем запрос к стороннему сервису
            weather_data = await get_weather_data(city)
            # Обновляем кэш
            update_cache(city, weather_data)
            await weather_db.insert_weather_data(city, weather_data)

        # Отправляем результат пользователю
        await message.answer(weather_data)
    else:
        await message.answer("Такого города нет в списке доступных. Введите другой город. /cities")

if __name__ == '__main__':
    from aiogram import executor

    # Подключение к базе данных
    loop = asyncio.get_event_loop()
    loop.run_until_complete(weather_db.connect())
    executor.start_polling(dp, skip_updates=True)
