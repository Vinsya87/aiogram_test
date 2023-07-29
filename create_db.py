import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Загружаем переменные окружения
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Функция для создания таблицы "weather_log" в базе данных
def create_weather_log_table():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS weather_log (
                    id SERIAL PRIMARY KEY,
                    city TEXT NOT NULL,
                    weather_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );''')
    conn.commit()
    conn.close()

# Вызываем функцию для создания таблицы при запуске приложения
if __name__ == '__main__':
    create_weather_log_table()
