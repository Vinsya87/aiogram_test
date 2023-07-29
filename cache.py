import time

# Кэш для хранения данных о погоде
weather_cache = {}


def is_cache_valid(city, cache_ttl):
    # Проверяем, есть ли данные о погоде для города в кэше
    if city in weather_cache:
        # Получаем время последнего обновления данных
        last_update_time = weather_cache[city]['timestamp']
        # Проверяем, не истекло ли время жизни кэша
        if time.time() - last_update_time < cache_ttl:
            return True
    return False


def update_cache(city, data):
    # Обновляем данные о погоде в кэше
    weather_cache[city] = {
        'data': data,
        'timestamp': time.time()
    }
