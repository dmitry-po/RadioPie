# Python 2.7.13
# -*- coding: utf-8 -*-

from time import sleep
from flask import Flask
from flask import render_template
from flask import request
import requests
import xml.etree.ElementTree as xmltree
import alarm
import mediaPlayer as mp
import subprocess
import os


# -->
OWM_appid = '58aaaed4b1fe9293916758ce54a05b94'
OWM_api = 'http://api.openweathermap.org/data/2.5/'
# <--

# 20.06.2018 add -->
player = mp.MediaPlayer()
new_alarm = alarm.Alarm('alarm', player)
player.start()
# 20.06.2018 add <--


def get_media(station):
    # media = instance.media_new(station)
    # return media
    ''

def init_params():
    try:
        selected_station = request.form['station']
    except:
        selected_station = 'http://ic7.101.ru:8000/a101'
    try:
        volume = int(request.form['volume_bar'])
    except:
        volume = 77
    return selected_station, volume


# -->
def get_weather(type='weather', city='Moscow', country='ru'):
    try:
        # type = ['weather','forecast]
        request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
        request_res = requests.get(request_link).json()
        print(request_res)
        weather = {'id':request_res['weather'][0]['id'],
                   'humidity': request_res['main']['humidity'],
                   'pressure': request_res['main']['pressure'],
                   'temp': round(request_res['main']['temp'] - 273, 1),
                   'temp_max': round(request_res['main']['temp_max'] - 273, 1),
                   'temp_min': round(request_res['main']['temp_min'] - 273, 1),
                   'icon': get_weather_icon(request_res['weather'][0]['id'])}
        #print(weather)
    # 21.06.2018 add -->
    except ConnectionError:
        print('Cant load weather forecast')
        weather = {'id':'',
                   'humidity': '',
                   'pressure': '',
                   'temp': '',
                   'temp_max': '',
                   'temp_min': '',
                   'icon': ''}
    # 21.06.2018 add <--
    return weather


def get_weather_forecast(type='forecast', city='Moscow', country='ru'):
    try:
        request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
        request_res = requests.get(request_link).json()
        request_res = request_res['list']
        weather = []
        for forecast in request_res:
            weather.append(
                {'id':forecast['weather'][0]['id'],
                 'humidity': forecast['main']['humidity'],
                 'pressure': forecast['main']['pressure'],
                 'temp': round(forecast['main']['temp'] - 273, 1),
                 'temp_max': round(forecast['main']['temp_max'] - 273, 1),
                 'temp_min': round(forecast['main']['temp_min'] - 273, 1),
                 'icon': get_weather_icon(forecast['weather'][0]['id']),
                 'date': forecast['dt_txt']}
                )
        #print(weather)
    except ConnectionError:
        weather = [{'id': '',
                   'humidity': '',
                   'pressure': '',
                   'temp': '',
                   'temp_max': '',
                   'temp_min': '',
                   'icon': ''}]
    return weather

def get_weather_icon(id):
    icon = ''
    if id > 800:
        icon = 'static/weather_icons/Cloud.svg'
    elif id == 800:
        icon = 'static/weather_icons/Sun.svg'
    elif id >= 700:
        icon = 'static/weather_icons/Cloud-Fog-Sun.svg'
    elif id >= 600:
        icon = 'static/weather_icons/Cloud-Snow.svg'
    elif id >= 500:
        icon = 'static/weather_icons/Cloud-Rain.svg'
    elif id >= 300:
        icon = 'static/weather_icons/Cloud-Drizzle.svg'
    elif id >= 200:
        icon = 'static/weather_icons/Cloud-Lightning.svg'
    return icon

def get_news():
    link = 'https://meduza.io/api/v3/search?chrono=news&locale=ru&page=0&per_page=1'
    news_titles = []
    try:
        request_res = requests.get(link).json()
        news_list = request_res['collection']
        for news in news_list:
            # news_p = '<p>{}</p>'.format(request_res['documents'])
            new_item = {'title':request_res['documents'][news]['title'],
                        'url':'http://meduza.io/'+request_res['documents'][news]['url']}
            news_titles.append(new_item)
    except:
        print('No news')
    return news_titles
# <--


# 21.06.2018 add -->
def get_stations():
    station_tree = xmltree.parse('params/stations.xml')
    stations = station_tree.getroot()
    playlist = []
    for station in stations:
        playlist.append([station[0].text, station[1].text])
    return playlist
# 21.06.2018 add <--


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_index_page():
    print('voila!') 
    selected_station, volume = init_params()
    styles = render_template('styles.css')

    # -->
    weather_today = get_weather()
    weather_forecast = get_weather_forecast()
    # <--
    
    if request.method=='POST':

        selected_station = request.form['station']
        # media = instance.media_new(selected_station)
        volume = int(request.form['volume_bar'])
        
        if request.form['submit'] == 'on':
            print(selected_station, volume)
            player.set_params(volume=volume)
            if not player.is_alive():
                # player.start()
                player.play()
            
            
        elif request.form['submit'] == 'off':
            # stop_music()
            player.kill_player()
            
        elif request.form['submit'] == 'test':
            print('set volume to {}'.format(volume))
            player.change_volume(volume)

    return render_template('index.html', name="Shine bright!",
                           styles=styles,
                           playlist=get_stations(),
                           selected_station = selected_station,
                           volume = volume,
                           weather = weather_today,
                           forecast = weather_forecast[:8],
                           news = get_news())


# 20.06.2018 add -->
@app.route('/alarm', methods=['GET', 'POST'])
def get_alarm_page():
    print('voila2!')
    selected_station, volume = init_params()
    styles = render_template('styles.css')
    # <--

    if request.method == 'POST':

        selected_station = request.form['station']
        # media = instance.media_new(selected_station)

        if request.form['submit'] == 'stop_alarm':
            new_alarm.stop_alarm()

        elif request.form['submit'] == 'set_alarm':
            print('r u here?')
            alarm_time = request.form['start_time']
            alarm_h = int(alarm_time[:2])
            alarm_m = int(alarm_time[3:])
            new_alarm.set_alarm(alarm_h,alarm_m,'empty')
            if not new_alarm.is_alive():
                new_alarm.start()
            # a = thread.start_new_thread(fire_alarm, (media, alarm_h, alarm_m))

    return render_template('alarm.html',
                           styles=styles,
                           playlist=get_stations(),
                           selected_station=selected_station,
                           current_alarm=new_alarm.get_next_alarm_time())
# 20.06.2018 add <--


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port='3000')
