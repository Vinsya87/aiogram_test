import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

class WeatherDatabase:
    def __init__(self):
        self.db_pool = None

    async def connect(self):
        self.db_pool = await asyncpg.create_pool(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
        )

    async def disconnect(self):
        if self.db_pool:
            await self.db_pool.close()

    async def insert_weather_data(self, city, weather_data):
        async with self.db_pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO weather_log (city, weather_data)
                VALUES ($1, $2)
                """,
                city, weather_data
            )

    async def get_weather_data_from_db(self):
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM weather_log")
            return rows