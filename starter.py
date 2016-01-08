#! /usr/bin/python

#        отступы табуляцией
#        by Andrew Sotniokv aka Luca Brasi, 
#        e-mail: andruha.sota@mail.ru
#        --------------

import subprocess, time

class Launch():
#    Интервал в секундах
    interval=3600
    start=19
    end=24
    
#   Возвращает значение текущего времени. Нужно передать аргументы формата
#   hm, h, m
    def getTime(self,format):
        if format == 'hm':
            t=time.strftime("%H:%M")
            print(t)
            return int(t)
        elif format == 'h':
            t=time.strftime("%H")
            print(t)
            return int(t)
        elif format == 'm':
            t=time.strftime("%M")
            print(t)
            return int(t)

__author__ = "andrew"
__date__ = "$07.01.2016 23:12:39$"

if __name__ == "__main__":
    time.sleep(80)    
    tasks=['play_eng.py']
    lanch=Launch()
#    lanch.start=11
    t=lanch.getTime('h')
    while t <= lanch.end:
        if t < lanch.start:
            print('Еще не вечер...')
            time.sleep(lanch.interval)
            continue
        subprocess.call('python3 '+tasks[0], shell=True)
        time.sleep(lanch.interval)
