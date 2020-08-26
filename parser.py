#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Парсинг RSS лент
"""


import sys
import requests
import feedparser
from json import loads
from time import mktime
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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


def parse_rss(str_: str, site: str) -> str:
    """Парсинг RSS лент"""

    feed = feedparser.parse(site)
    str_ = ''

    for article in feed['entries']:
        # Если пост есть в БД, не отправляем его
        if database.article_in_db(article['title'], article['published']):
            continue
        # Добавляем пост в БД
        database.add_article_to_db(article['title'], article['published'])
        title = article['title']
        published = datetime.fromtimestamp(mktime(article['published_parsed'])) + timedelta(hours=3)
        link = article['link']

        str_ += f'*{title.replace("&amp;", "&")}*\nОпубликовано: _{published}_\n[Ссылка]({link})\n\n'

    return str_ or 'Новых постов нет'


def weather() -> str:
    """Погода с OpenWeatherMap"""

    _params = {'id': config.CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': config.APP_ID}
    res = requests.get(config.OWM, params=_params)

    data = res.json()

    if data['cod'] != 200:
        return f'Не удалось получить погоду\nПричина:\n{data["message"]}'

    tmpr = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_ = data['weather'][0]['description']
    main_weather_icon = config.WEATHER_ICONS.get(data['weather'][0]['main'])
    weather_ = weather_[0].upper() + weather_[1:] if len(weather_) > 1 else weather_
    wind = data['wind']['speed']
    humidity = data['main']['humidity']

    return f'*Погода в Костроме*\n{main_weather_icon*5}\n_{weather_}_\n\
        Температура воздуха: `{tmpr}°`\nОщущается как: `{feels_like}°`\n\
        Скорость ветра: `{wind} м/с`\nВлажность: `{humidity}%`'


def coronavirus() -> str:
    """Информация о коронавирусе"""

    url = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/'
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')

    header = soup.find('h1', class_='cv-section__title_mobile-small').text
    stats_item = soup.find('cv-stats-virus')
    stats = loads(stats_item.attrs.get(':stats-data')) if stats_item else None

    if stats:
        return f'{header}\nВыявлено заболевших: `{stats.get("sick")}`\n\
            Выявлено заболевших за сутки: `{stats.get("sickChange")}`\n\
            Человек выздоровело: `{stats.get("healed")}`\n\
            Человек выздоровело за сутки: `{stats.get("healedChange")}`\n\
            Человек умерло: `{stats.get("died")}`\n\
            Человек умерло за сутки: `{stats.get("diedChange")}`\n'

    return 'Не удалось получить информацию о коронавирусе'


if __name__ == '__main__':
    result = coronavirus()
    if sys.argv[1] == 'weather':
        send(weather())
    elif sys.argv[1] == 'habr':
        send(parse_rss('*Новые посты на Habr:*\n\n', config.HABR))
    elif sys.argv[1] == 'dtf':
        send(parse_rss('*Новые посты на DTF:*\n\n', config.DTF))
    elif sys.argv[1] == 'coronavirus':
        send(coronavirus())
