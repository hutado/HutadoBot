"""
Feed telegram bot
"""


import sys
import requests
import feedparser
from datetime import datetime, timedelta
from time import mktime

import config
import database


def send(message: str) -> requests.Response:
    """Отправка сообщений в телеграм"""

    return requests.get(
        config.SEND_TEXT,
        params=[
            ('parse_mode', 'Markdown'),
            ('disable_web_page_preview', True),
            ('text', message)
        ]
    )


def parse_rss(str_: str, site: str) -> requests.Response:
    """Парсинг RSS лент"""

    exists = False
    feed = feedparser.parse(site)

    for article in feed['entries']:
        # Если пост есть в БД, не отправляем его
        if database.article_in_db(article['title'], article['published']):
            continue
        # Добавляем пост в БД
        database.add_article_to_db(article['title'], article['published'])
        exists = True
        title = article['title']
        published = datetime.fromtimestamp(mktime(article['published_parsed'])) + timedelta(hours=3)
        link = article['link']

        str_ += '*{}*\nОпубликовано: _{}_\n[Ссылка]({})\n\n'.format(title.replace('&amp;', '&'), published, link)

    return send(str_) if exists else None


def weather() -> requests.Response:
    """Погода с OpenWeatherMap"""

    res = requests.get(config.OWM, params={'id': config.CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': config.APP_ID})

    data = res.json()

    if data['cod'] != 200:
        message = 'Не удалось получить погоду\nПричина:\n{}'.format(data['message'])
        return send(message)

    city = data['name']
    tmpr = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_ = data['weather'][0]['description']
    main_weather_icon = config.WEATHER_ICONS.get(data['weather'][0]['main'])
    weather_ = weather_[0].upper() + weather_[1:] if len(weather_) > 1 else weather_
    wind = data['wind']['speed']
    humidity = data['main']['humidity']

    str_ = '*Погода {}*\n{}\n_{}_\nТемпература воздуха: `{}°`\nОщущается как: `{}°`\nСкорость ветра: `{} м/с`\n'\
        'Влажность: `{}%`'.format(city, main_weather_icon*5, weather_, tmpr, feels_like, wind, humidity)

    return send(str_)


if __name__ == '__main__':
    if sys.argv[1] == 'weather':
        weather()
    elif sys.argv[1] == 'habr':
        parse_rss('*Новые посты на Habr:*\n\n', config.HABR)
    elif sys.argv[1] == 'dtf':
        parse_rss('*Новые посты на DTF:*\n\n', config.DTF)
