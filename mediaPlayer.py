from threading import Thread
from subprocess import Popen, PIPE
import os
import time

class MediaPlayer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.is_active = False
        """something happens here"""

    def run(self, volume=90, volume_raise=False):
        # os.system('omxplayer -o both http://ic7.101.ru:8000/a101')
        self.process = Popen(['omxplayer', '-o', 'both', '--vol', '-3000', 'http://ic7.101.ru:8000/a101'],
                             stdout=None, stdin=PIPE)
        print('Let the music play')
        self.raise_volume()

    def stop(self):
        print('Oh, shit')
        self.process.stdin.write('-')
        # print(stdout)
        # self.process.communicate('q')
        # os.system('omxplayer q')

    def raise_volume(self):
        vol=-10
        while vol<0:
            print(vol)
            self.process.stdin.write('+')
            # (stdout, stder) = self.process.communicate('+')
            vol+=1
            time.sleep(5)
            
