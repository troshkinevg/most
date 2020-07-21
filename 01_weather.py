# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database

import click
import requests
import datetime as dt
import os
import lxml.html
import cv2

from work_with_online_services import Prediction
from work_with_graphics import ImageMaker
from work_with_the_database import DatabaseUpdater

time_response = requests.get('https://pogoda.63.ru/')
HTML_TREE = lxml.html.document_fromstring(time_response.text)

IMAGE = cv2.imread("python_snippets/external_data/probe.jpg")

path = os.path.join(os.path.dirname(__file__), 'database.db')
DATABASE_DIRECTORY = os.path.normpath(path)

WHITE = [255, 255, 255]
YELLOW = [0, 255, 255]
BLUE = [138, 83, 0]
LIGHT_BLUE = [255, 191, 0]
GRAY = [177, 205, 205]

BOX = {
    'weather': {
        'Пасмурно, дождь': [BLUE, 'python_snippets/external_data/weather_img/rain.jpg'],
        'Пасмурно, без осадков': [BLUE, 'python_snippets/external_data/weather_img/rain.jpg'],
        'Облачно, без осадков': [GRAY, 'python_snippets/external_data/weather_img/cloud.jpg'],
        'Облачно, дождь': [GRAY, 'python_snippets/external_data/weather_img/cloud.jpg'],
        'Ясная погода, без осадков': [YELLOW, 'python_snippets/external_data/weather_img/sun.jpg'],
        'Переменная облачность, без осадков': [LIGHT_BLUE, 'python_snippets/external_data/weather_img/snow.jpg']
    }
}


@click.group()
def cli():
    pass


@click.option('--dates', nargs=2, type=str, help='Формат даты: ГОД, МЕСЯЦ, ДЕНЬ')
@cli.command()
def watch_the_period_of_days(dates):
    st = dates[0].split(',')
    se = dates[1].split(',')
    first = dt.date(year=int(st[0]), month=int(st[1]), day=int(st[2]))
    second = dt.date(year=int(se[0]), month=int(se[1]), day=int(se[2]))
    create = Prediction(html_tree=HTML_TREE)
    third = DatabaseUpdater(directory=DATABASE_DIRECTORY, three_days=create.new())
    for day in third.new_create().select():
        if second >= day.date >= first:
            print(day.date, day.weather, day.temperature)


@cli.command()
def add_to_dt():
    days = []
    create = Prediction(html_tree=HTML_TREE)
    third = DatabaseUpdater(directory=DATABASE_DIRECTORY, three_days=create.new())
    for day in third.new_create().select():
        days.append(day.date)
    for day in third.three_days:
        if day['date'] not in days:
            third.write_to_database(day)


@cli.command()
def draw_postcards():
    create = Prediction(html_tree=HTML_TREE)
    mew = ImageMaker(current_readings=create.new(), image=IMAGE, box=BOX)
    mew.create_a_postcard()


@cli.command()
def view_weather():
    create = Prediction(html_tree=HTML_TREE)
    for day in create.new():
        print(str(day['date']), day['temperature'], day['weather'])


if __name__ == '__main__':
    cli()
