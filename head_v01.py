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

playlist = [['http://ic7.101.ru:8000/a200', 'Relax'],
            ['http://ic7.101.ru:8000/a202', 'Comedy'],
            ['http://ic7.101.ru:8000/a101', 'Romantic'],
            ['http://185.39.195.90:8000/montecarlo_128', 'Monte Carlo']]
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()

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


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def smth():
    print('voila!') 
    selected_station, volume = init_params()
    styles = render_template('styles.css')
    
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

            
    return render_template('index.html', name="it's alive!",
                           styles=styles,
                           playlist = playlist,
                           selected_station = selected_station,
                           volume = volume)


if __name__ == "__main__":
    app.run()
