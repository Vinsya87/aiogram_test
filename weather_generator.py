import random


def generate_weather_data():
    temperature = random.randint(-20, 30)
    wind_speed = random.randint(0, 20)
    wind_directions = ['С', 'СЗ', 'З', 'ЮЗ', 'Ю', 'ЮВ', 'В', 'СВ']
    wind_direction = random.choice(wind_directions)
    precipitation = random.choice(['Без осадков', 'Дождь', 'Снег', 'Град'])

    return temperature, wind_speed, wind_direction, precipitation
