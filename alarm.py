# 20.06.2018 make alarm class -->
from threading import Thread
import time


class Alarm_timer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        ''


class Alarm(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.is_active = False

    def set_alarm(self, hour, minute, media):
        print('got here')
        self.next_alarm_time = [hour, minute]
        print('still here')
        self.alarm_media = media
        self.is_active = True
        self.get_next_alarm_time()
        # self.fire_alarm()

    def stop_alarm(self):
        self.is_active = False

    def get_next_alarm_time(self):
        if self.is_active:
            res = "Next alarm in {0}:{1}".format(self.next_alarm_time[0],
                                                 self.next_alarm_time[1])
        else:
            res = 'You are happy man!'
        print(res)
        return res

    def run(self):
        while True:
            while self.is_active:
                current_time = time.localtime()
                print('current: {0}:{1}, active={2}'.format(current_time.tm_hour,
                                                            current_time.tm_min,
                                                            self.is_active))
                if ((current_time.tm_hour == self.next_alarm_time[0]) &
                        (current_time.tm_min == self.next_alarm_time[1])):
                    self.play_alarm()
                else:
                    print('sleep')
                    time.sleep(10)
            print('alarm not active')
            time.sleep(10)


    def play_alarm(self):
        volume = 0
        # player.play()
        while volume < 90:
            # player.audio_set_volume(volume)
            print(volume)
            time.sleep(1)
            volume += 1

    def fire_alarm(self):
        # 20.06.2018 comment -->
        '''
        volume = 0
        player.audio_set_volume(volume)
        player.stop()
        player.set_media(media)

        # 20.06.2018 comment <--
        # print('start at {0}:{1}'.format(hour, minute))
        # remake trigger -->
        current_time = time.localtime()
        sleep_duration_m = 24 * 60 + (hour * 60 + minute -
                                      (current_time.tm_hour * 60 + current_time.tm_min))
        start_in_h = (sleep_duration_m // 60) % 24
        start_in_m = sleep_duration_m % 60
        print('start in {0}:{1}'.format(start_in_h, start_in_m))
        sleep_duration = start_in_h * 3600 + start_in_m * 60
        print(sleep_duration)
        sleep(sleep_duration)
        '''
        # remake trigger <--
# 20.06.2018 make alarm class <--
