#! /usr/bin/python3

#    Все эти манипуляции призваны для улучшения английского. Запускается файл 
#    на проигрывание в фоновом режиме. По желанию сопровождается текстом.
#
#    	sudo apt-get install python3-tk
#
#    отступы табуляцией
#    by Luca Brasi, e-mail: andrew.sotnikov@zoho.com
#    --------------

import subprocess, os, re, time, threading
from tkinter.messagebox import *
from tkinter import *
from random import randint


class View:
#    Рисует маленькое окошко для выбора PDF
    def draw(self):
        self.root=Tk()
        windows= Frame(self.root,width=100,heigh=100)
        windows.pack()
        self.root.title('Выбирай')
        lb1=Label(windows,text='   Читать PDF будешь?   ',font='arial 16')
        lb1.grid(row=0,column=0,columnspan=2)
        lb1=Label(windows,text='  ',font='arial 16')
        lb1.grid(row=1,column=0,columnspan=2)
        bt1=Button(windows,text='Yes',width=5,height=1,font='arial 14',command=self.openPDF)
        bt1.grid(row=2,column=0)
        bt2=Button(windows,text='No',width=5,height=1,font='arial 14', command=self.closeMain)
        bt2.grid(row=2,column=1)
        self.root.mainloop()
    
#    Закрывает окно
    def closeMain(self):
        self.root.quit()
        self.root.withdraw()
        delattr(self, 'root') 

#   Запускает PDF файл, а потом закрывает окно    
    def openPDF(self):
        fullpath=self.path+self.chosenPDF
        subprocess.call('okular '+fullpath,shell=True)
        self.root.quit()
        self.root.withdraw()
        delattr(self, 'root') 
        
#    Принудительно закрывает окно
    def forceStop(self):
        time.sleep(420)   # Задержка после которой закрывается окно
        try:
            if (self.root):
                self.closeMain()
        except AttributeError:
            print('Опачки, кажеться окошко уже удалили!')            
    
class PlayBBC(View):
#    Абсолютный путь к папке с музыкой
    path='/media/Maindata/Дело/English/BBC/English_we_speak/'
#    Количество повторов песни подряд
    repeats=3
    
    def __init__(self):
        self.all_files=os.listdir(self.path)
        self.pdf=[]
        self.mp3=[]
        for elem in self.all_files:
            pattern_mp3=re.search(r"(mp3)$",elem)
            pattern_pdf=re.search(r"(pdf)$",elem)
            if pattern_mp3:
                self.mp3.append(elem)
            elif pattern_pdf:
                self.pdf.append(elem)

#    Генерирует случайное число на основании списка файлов mp3. Подискивает 
#    такой же pdf файл. Если нет абсолютного соответсвия mp3 и pdf - ищет снова.
#    И так до тех пор пока не будет полного соответсвия. Возвращает имена 
#    файлов mp3 и pdf.
    def getNumber(self):
        randLimit=len(self.mp3)
        running=True
        while running==True:
            randNumb=(randint(1,randLimit))-1
            mp3=self.mp3[randNumb]
            pattern=re.compile(r''+mp3[0:6]+'')
            for elem in self.pdf:
                pdf=elem
                if(pattern.search(elem)):
                    running=False
                    break
        print('mp3= ',mp3,'\npdf= ',pdf)
        return(mp3,pdf)

#    Играет песню
    def playSong(self,song):
        fullPath=self.path+song
        print(fullPath)
        for x in range(self.repeats):
            subprocess.call('mplayer '+fullPath,shell=True)
            
    def fThStarter(self):
        files=self.getNumber()
        self.chosenPDF=files[1]
        self.playSong(files[0])
        

class Launch():
#    Интервал в секундах
    interval=5
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
    
class Log(PlayBBC):
    def __init__(self):

        PlayBBC.__init__(self)

    #    Путь к log файлу
        self.log_file='/var/log/andrew/play_eng.log'
        
    #   Просто открывает файл и пишет туда сообщения
    def writeToLogFile(self):
#       Текст сообщения который будет записан в лог
        self.message=(time.strftime("%d-%m-%Y %H:%M:%S   "))+ 'Запуск был успешный. BBC-\"English we speak\"   '+ self.chosenPDF[:-4] +'\"\n'

        f=open(self.log_file, 'a')
        f.write(self.message)
        print('Лог записан!')
        f.close()
        

if __name__ == "__main__":

    play=Log()
#   Можно указать количество повторов        
#   play.repeats=1      
#   Созданы потоки для запуска player и GUI
#    ---------
    th1 = threading.Thread(target=play.fThStarter)
    th2 = threading.Thread(target=play.draw)
    th1.start()
    th2.start()
    play.forceStop() #Принудительно убиваем окно, если вдруг лень было закрыть
    th1.join()
    th2.join()
#   ---------


#   Пишем в лог результаты 
    play.writeToLogFile()

