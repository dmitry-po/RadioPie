# Python 2.7.13
# -*- coding: utf-8 -*-

import vlc
import time
from time import sleep
from flask import Flask
from flask import render_template
from flask import request
import threading
import thread
# -->
import requests
# <--

playlist = [['http://ic7.101.ru:8000/a200', 'Relax'],
            ['http://ic7.101.ru:8000/a202', 'Comedy'],
            ['http://ic7.101.ru:8000/a101', 'Romantic'],
            ['http://185.39.195.90:8000/montecarlo_128', 'Royal']]
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
# -->
OWM_appid = '58aaaed4b1fe9293916758ce54a05b94'
OWM_api = 'http://api.openweathermap.org/data/2.5/'
# <--

def fire_alarm(media, hour, minute):
    volume = 0
    player.audio_set_volume(volume)  
    player.stop()
    player.set_media(media)
    print('start at {0}:{1}'.format(hour, minute))
    # remake trigger -->
    current_time = time.localtime()
    sleep_duration_m = 24*60 + (hour*60 + minute -
                                (current_time.tm_hour*60 + current_time.tm_min))
    start_in_h = (sleep_duration_m // 60) % 24
    start_in_m = sleep_duration_m % 60
    print('start in {0}:{1}'.format(start_in_h, start_in_m))
    sleep_duration = start_in_h*3600 + start_in_m*60
    print(sleep_duration)
    sleep(sleep_duration)
    # remake trigger <--
    player.play()
    while volume < 90:
        player.audio_set_volume(volume)
        print(volume)
        sleep(1)
        volume += 1
        

def test_play(media, volume):
    # player.stop()   
    player.set_media(media)
    #print(player.is_playing())
    if player.is_playing != 1:
        player.play()
        print('started')
    player.audio_set_volume(volume)
    
    print('Let the music play')

def stop_music():
    player.stop()
    print('oh no!')

def test():
    print(request.form['start_time'])

def get_media(station):
    media = instance.media_new(station)
    return media

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
    # type = ['weather','forecast]
    request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
    request_res = requests.get(request_link).json()
    print(request_res)
    weather = {'id':request_res['weather'][0]['id'],
               'humidity': request_res['main']['humidity'],
               'pressure': request_res['main']['pressure'],
               'temp': request_res['main']['temp'] - 273,
               'temp_max': request_res['main']['temp_max'] - 273,
               'temp_min': request_res['main']['temp_min'] - 273,
               'icon': get_weather_icon(request_res['weather'][0]['id'])}
    print(weather)
    return weather

def get_weather_forecast(type='forecast', city='Moscow', country='ru'):
    request_link = OWM_api + type + '?&q={0},{1}&appid={2}'.format(city, country, OWM_appid)
    request_res = requests.get(request_link).json()
    request_res = request_res['list']
    weather = []
    for forecast in request_res:
        #print('---')
        #print(forecast)
        #print('+++')
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
    


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def smth():
    print('voila!') 
    selected_station, volume = init_params()
    # change styles -->
    styles = render_template('styles.css')
    styles = ''
    # <--

    # -->
    weather_today = get_weather()
    weather_forecast = get_weather_forecast()
    # <--
    
    if request.method=='POST':

        selected_station = request.form['station']
        media = instance.media_new(selected_station)
        volume = int(request.form['volume_bar'])
        
        if request.form['submit'] == 'on':
            print(selected_station, volume)
            test_play(media, volume)
            player.audio_set_volume(volume)
            
        elif request.form['submit'] == 'off':
            stop_music()
            
        elif request.form['submit'] == 'alarm':
            alarm_time = request.form['start_time']
            alarm_h = int(alarm_time[:2])
            alarm_m = int(alarm_time[3:])
            a = thread.start_new_thread(fire_alarm, (media, alarm_h, alarm_m))

            
        elif request.form['submit'] == 'test':
            # print(request.form['volume_bar'])
            player.audio_set_volume(volume)
            print('hey!')
            print(player.is_playing())
            # player.will_play()

            
    return render_template('index.html', name="Shine bright!",
                           styles=styles,
                           playlist = playlist,
                           selected_station = selected_station,
                           volume = volume,
                           weather = weather_today,
                           forecast = weather_forecast[:8],
                           news = get_news())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
