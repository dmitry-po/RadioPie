#!/usr/bin/env python
# -*- coding:utf-8 -*-

from time import sleep
from flask import Flask
from flask import render_template
from flask import request
import threading

# 25.04.2018 add -->
import requests
# 25.04.2018 add <--

url = 'http://91.207.59.26/a200'
playlist = [['http://91.207.59.26/a101', 'Romantic'],
            ['http://91.207.59.26/a105', 'Something1'],
            ['http://91.207.59.26/a109', 'Something2'],
            ['http://91.207.59.26/a200', 'Relax'],
            ['http://91.207.59.26/a202', 'Comedy']]
selected_station = ''
# 25.04.2018 add -->
OWM_appid = '58aaaed4b1fe9293916758ce54a05b94'
OWM_api = 'http://api.openweathermap.org/data/2.5/'
# 25.04.2018 add <--

def timer_shoot():
    print('bang!')


def main():
    print('Im working')
    sleep(3)
    print('Bye!')
    threading.Timer(10, timer_shoot).start()
    print('hey!')


# 25.04.2018 add -->
def get_weather(type='weather', city='Moscow', country='ru'):
    # type = ['weather','forecast]
    request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
    # print(request_link)
    request_res = requests.get(request_link).json()
    print(request_res)
    weather = {'id':request_res['weather'][0]['id'],
               'humidity': request_res['main']['humidity'],
               'pressure': request_res['main']['pressure'],
               'temp': request_res['main']['temp'] - 273,
               'temp_max': request_res['main']['temp_max'] - 273,
               'temp_min': request_res['main']['temp_min'] - 273}
    print(weather)
    return weather


def get_weather_icon(id):
    icon = ''
    if id == 803:
        icon = 'static/weather_icons/Cloud.svg'
    elif id == 520:
        icon = 'static/weather_icons/Cloud-Rain.svg'
    return icon
# 25.04.2018 add <--

# 25.04.2018 add -->
def get_news():
    link = 'https://meduza.io/api/v3/search?chrono=news&locale=ru&page=0&per_page=1'
    request_res = requests.get(link).json()
    news_list = request_res['collection']
    news_titles = []
    for news in news_list:
        # news_p = '<p>{}</p>'.format(request_res['documents'])
        news_titles.append(request_res['documents'][news]['title'])
    print(news_titles)
    return news_titles

# 25.04.2018 add <--

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hllwrld(name='smth'):
    if request.method == 'POST':
        if request.form['submit'] == 'play':
            main()
            print('play')
        elif request.form['submit'] == 'stop':
            print('stop')
        elif request.form['submit'] == 'test':
            print('test')
            # 25.04.2018 add -->
            weather = get_weather()
            # 25.04.2018 add <--
    # 25.04.2018 upd -->
    return render_template('interface.html', name=name, stations=playlist,
                           weather=[], weather_icon='',
                           news=get_news())
    '''
    return render_template('interface.html', name=name, stations=playlist,
                               selected_station=a))
    '''
    # 25.04.2018 upd <--


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234, debug=True)
    #app.run()
