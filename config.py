"""
Конфигурация бота
"""


import os


# RSS ленты
HABR = 'https://habr.com/ru/rss/all/top100/?fl=ru'
DTF = 'https://dtf.ru/rss/new'

# OpenWeatherMap
OWM = "http://api.openweathermap.org/data/2.5/weather"

# Для работы бота необходиы следующие переменные окружения:
# Токен телеграм бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# ChatID получателя
RECEIVER = os.environ.get('RECEIVER')
# ID города, где требуется получить погоду
CITY_ID = os.environ.get('CITY_ID')
# API-ключ от OWM
APP_ID = os.environ.get('APP_ID')

# Get-запрос для отправки сообщения в телеграм
SEND_TEXT = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}'.format(BOT_TOKEN, RECEIVER)

# База данных SQLite3
DATABASE = os.path.dirname(os.path.abspath(__file__)) + '/hutado.db'

# Emoji погоды
WEATHER_ICONS = {
    'Clouds': u'\U00002601',
    'Clear': u'\U00002600',
    'Atmosphere': u'\U0001F32B',
    'Snow': u'\U00002744',
    'Rain': u'\U0001F327',
    'Drizzle': u'\U0001F327',
    'Thunderstorm': u'\U0001F329'
}
