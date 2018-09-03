from threading import Thread
from subprocess import Popen, PIPE
import os
import time

class MediaPlayer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.is_active = False
        self.volume = 0
        self.fade_in = False
        """something happens here"""

    def run(self):
        station = 'http://ic7.101.ru:8000/a101'
        if self.fade_in:
            self.volume = -1000
        self.process = Popen(['omxplayer', '-o', 'both', '--vol', '{}'.format(self.volume), '{}'.format(station)],
                             stdout=None, stdin=PIPE)
        print('Let the music play "{}"'.format(station))
        if self.fade_in:
            self.raise_volume()

    def stop(self):
        print('Oh, shit')
        self.process.stdin.write('-')
        # self.process.stdin.write('q')


    def pause(self):
        print('pause player')
        self.process.stdin.write('p')

    def set_params(self, volume=0, fade_in=False):
        self.volume=volume
        self.fade_in = fade_in

    def raise_volume(self):
        while self.volume<0:
            print(self.volume)
            self.process.stdin.write('+')
            self.volume+=100
            # time.sleep(60)
            time.sleep(15)

    def set_volume(self, new_volume):
        while self.volume < new_volume:
            self.process.stdin.write('+')
            self.volume += 100
        while self.volume > new_volume:
            self.process.stdin.write('-')
            self.volume -=100
        
            
