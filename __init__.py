# Python 2.7.13
# -*- coding: utf-8 -*-

# 20.06.2018 replace -->
debug = True
if not debug:
    import vlc
# import vlc
# 20.06.2018 replace <--
import time
from time import sleep
from flask import Flask
from flask import render_template
from flask import request
import threading
# 20.06.2018 comment -->
# import thread
# 20.06.2018 comment <--
# -->
import requests
# 20.06.2018 add -->
import alarm
import xml.etree.ElementTree as xmltree
# 20.06.2018 add <--
# 25072018 add -->
import mediaPlayer as mp
# 25072018 add <--
# 07082018 -->
import subprocess
import os
# 07082018 <--
# <--

if not debug:
    instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    player = instance.media_player_new()
# -->
OWM_appid = '58aaaed4b1fe9293916758ce54a05b94'
OWM_api = 'http://api.openweathermap.org/data/2.5/'
# <--

# 20.06.2018 add -->
new_alarm = alarm.Alarm('alarm')
player = mp.MediaPlayer()
# 20.06.2018 add <--


def test_play(media, volume):
    # player.stop()   
    # player.set_media(media)
    # print(player.is_playing())
    # if player.is_playing != 1:
    #     player.play()
    #     print('started')
    # player.audio_set_volume(volume)
    
    print('Let the music play')

def stop_music():
    # player.stop()
    print('oh no!')

def test():
    print(request.form['start_time'])

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
    # 21.06.2018 replace -->
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
    '''
    request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
    request_res = requests.get(request_link).json()
    request_res = request_res['list']
    weather = []
    for forecast in request_res:
        weather.append(
            {'id':forecast['weather'][0]['id'],
             'humidity': forecast['main']['humidity'],
             'pressure': forecast['main']['pressure'],
             'temp': forecast['main']['temp'] - 273,
             'temp_max': forecast['main']['temp_max'] - 273,
             'temp_min': forecast['main']['temp_min'] - 273,
             'icon': get_weather_icon(forecast['weather'][0]['id']),
             'date': forecast['dt_txt']}
            )
    print(weather)
    return weather
    '''
# 21.06.2018 replace <--


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
    request_res = requests.get(link).json()
    news_list = request_res['collection']
    news_titles = []
    for news in news_list:
        # news_p = '<p>{}</p>'.format(request_res['documents'])
        news_titles.append(request_res['documents'][news]['title'])
    # print(news_titles)
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
                player.start()
            
            
        elif request.form['submit'] == 'off':
            # stop_music()
            player.pause()
            
        elif request.form['submit'] == 'test':
            print('set volume to {}'.format(volume))
            player.set_volume(volume)

        # 21.06.2018 delete -->
        '''
        elif request.form['submit'] == 'alarm':
                    alarm_time = request.form['start_time']
                    alarm_h = int(alarm_time[:2])
                    alarm_m = int(alarm_time[3:])
                    # a = thread.start_new_thread(fire_alarm, (media, alarm_h, alarm_m))
        '''
        # 21.06.2018 delete <--
            
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
