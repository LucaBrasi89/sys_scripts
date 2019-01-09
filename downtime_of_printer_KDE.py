#!/usr/bin/python3

#        отступы пробелами
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andrew.sotnikov@zoho.com
#        --------------
#        Определяет дефолтный принтер и смотрит сколко дней прошло
#        с последнего момента печати. Если больше 4ех дней посылает
#        окошко warnings, больше 7ми - critical.
#        *** KDE - VERSION !!! ***

import os,re, time, sys
from subprocess import *
from PyQt5 import QtWidgets, QtCore, QtGui

# Открывает исходный файл и возващает его в реверсированном порядке.
# Принимает аргументы: filename - путь к файлу, replace=True - заменит
# исходный файл на реверсированный.

#     ################  ВАЖНО!  ##############
#    Если при выводе:    
#        lpstat -W completed
#    последняя печать идет в начале, удали строку 33 ( ls=ls.reverse()).
#    Если последний сеанс печати в конце - ничего не трогай.

class ReverseFile:
    def __init__(self,filename,replace=False):
        self.doJobList()
        f1=open(filename)
        f2=open(filename+'_tmp','w')
        ls=[]
        for x in f1:
            ls.append(x)
#        ls=reversed(ls)
        for x in ls:
            f2.write(x)

        f1.close()
        f2.close()
        if replace==True:
            os.remove(filename)
            os.rename((filename+'_tmp'),filename)

    def doJobList(self):
        os.chdir('/tmp/')
        call('lpstat -W completed > ended_tasks', shell=True)

class getInfo():

    year={'jan':31,'feb':28,'mar':31,
          'apr':30,'may':31,'jun':30,
          'jul':31,'aug':31,'sep':30,
          'oct':31,'nov':30,'dec':31}

    month=('jan','feb','mar','apr','may','jun',
           'jul','aug','sep','oct','nov','dec')

    # Вызывает lpstat -d и парсит вывод.
    # Возвращает дефолтный имя дефолтного принтера.
    def getDefPrinter(self):
        pattern=check_output(['lpstat -d'],shell=True);pattern=str(pattern)
        res=re.search(r'(?<=:\s).+?(?=\\n)',pattern)
        printer=res.group(0)
        print('Твой дефолтный принтер - {0}'.format(printer))
        return printer


    def getPrLastDate(self):
        printer=self.getDefPrinter()
        f2=open('/tmp/ended_tasks')
        for x in f2:
            if (re.search(printer,x)) != None:
                print(x)
                break
        f2.close()
        date=self.parseDate(x)
        self.getDifference(date)



    # Получает строку формата:
    # Canon_E464-5            andrew          133120   Wed Dec 12 18:19:41 2018
    # Парсит string и возврщает список date, такого формата:
    # ('Dec', '12', '2018')
    def parseDate(self,string):
        date=re.search(r'(.{3})\s{1,}(\d{,2})\s{1,}(.{8})\s([0-9]{4})$',
                       string)
        date=date.group(1,2,4)
        print(date)
        return date

    # Получает количество дней с момента последнего запуска принтера и
    # возвращает это значение.
    # mm-dd-YYYY
    def getDifference(self,date):

        # Начало получения количества дней с момента последнего запуска
        d_from_last=0
        for x in self.month:
            if date[0].lower() in x:
                d_from_last = d_from_last + int(date[1])
                break
            d_from_last = d_from_last + self.year[x]
        # Конец получения количества дней с момента последнего запуска

        doy=int(time.strftime('%j',time.gmtime()))
        year=int(time.strftime('%Y',time.gmtime()))
        if (int(date[2])) != year:
            doy = doy + 365
        days_difference = doy - d_from_last
        print('Печать не проводилась {0} дней'.format(days_difference))
        self.days = days_difference

        # Окошко warnings
class DrawWarning(QtWidgets.QWidget):
    def __init__(self,days, parent=None,):
        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(960, 540, 300, 150)
        self.setWindowTitle('printer')
        font=QtGui.QFont()
        font.setPointSize(14)
        self.setFont(font)

        button_ok=QtWidgets.QPushButton('OK',self)

        button_ok.setFixedSize(100,40)

        button_ok.clicked.connect(self.close)

        label=QtWidgets.QLabel('You don\'t print for a {0} '
              'days'.format(days))
        label2=QtWidgets.QLabel()
        pixmap=QtGui.QPixmap('/usr/share/icons/oxygen/base/48x48/status/' \
                             'dialog-warning.png')
        label2.setPixmap(pixmap)

        grid=QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.setVerticalSpacing(20)
        grid.addWidget(label2,0,0,QtCore.Qt.AlignHCenter)
        grid.addWidget(label,1,0,QtCore.Qt.AlignHCenter)
        grid.addWidget(button_ok,2,0,1,1,QtCore.Qt.AlignHCenter)
        self.setLayout(grid)
        self.center()

        # Центрирует окно
    def center(self):

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-
        size.height())/2)

        # Окошко critical
class DrawCritical(DrawWarning):

    def __init__(self,days, parent=None,):
        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(960, 540, 300, 150)
        self.setWindowTitle('printer')
        font=QtGui.QFont()
        font.setPointSize(14)
        self.setFont(font)

        button_ok=QtWidgets.QPushButton('OK',self)

        button_ok.setFixedSize(100,40)
        button_ok.clicked.connect(self.close)
        label=QtWidgets.QLabel('You don\'t print for a {0} '
              'days.\n       Do it immediately!'.format(days))
        label2=QtWidgets.QLabel()
        pixmap=QtGui.QPixmap('/usr/share/icons/oxygen/base/48x48/' \
                             'status/dialog-error.png')
        label2.setPixmap(pixmap)

        grid=QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.setVerticalSpacing(20)
        grid.addWidget(label2,0,0,QtCore.Qt.AlignHCenter)
        grid.addWidget(label,1,0,QtCore.Qt.AlignHCenter)
        grid.addWidget(button_ok,2,0,1,1,QtCore.Qt.AlignHCenter)
        self.setLayout(grid)
        self.center()


if __name__ == "__main__":

    a=ReverseFile('/tmp/ended_tasks',replace=True)
    b=getInfo()
#    import pdb; pdb.set_trace()
    b.getPrLastDate()
    days=b.days

    app = QtWidgets.QApplication(sys.argv)
    if days >= 3 and days < 7:
        qb = DrawWarning(days)
    elif days >= 7:
        qb = DrawCritical(days)
    try:
        qb.show()
        sys.exit(app.exec_())
    except Exception:
        pass
