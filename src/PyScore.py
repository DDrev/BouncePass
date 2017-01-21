# -*- coding: UTF-8 -*-

from Tkinter import *
import ttk
import serial
import caspartalk
import socket


class Scorer(object):
    def __init__(self, parent):
        """
        :param parent: Parent widget
        """
        self.parent = parent

# Main containing frame
        self.appframe = ttk.Frame(parent, padding="5")
        self.appframe.grid(column=0, row=0)
        
        # self.casparinst = caspartalk.CasparServer()

# Frame collecting sport and TV feed version settings
        self.sportframe = ttk.Frame(self.appframe, padding='5')
        self.sportframe.grid(column=0, row=0)
        
        self.sportver = StringVar()
        self.sportver.set('bbr0')

        self.bbr0 = ttk.Radiobutton(self.sportframe, text="Basketball Rev0", variable=self.sportver, value='bbr0')
        self.bbr0.grid(column=0, row=0)
        self.bbr1 = ttk.Radiobutton(self.sportframe, text="Basketball Rev1", variable=self.sportver, value='bbr1')
        self.bbr1.grid(column=0, row=1)
        self.bbr2 = ttk.Radiobutton(self.sportframe, text="Basketball Rev2", variable=self.sportver, value='bbr2')
        self.bbr2.grid(column=0, row=2)
        # self.sportlabel = ttk.Label(self.sportframe, textvariable=self.sportver)
        # self.sportlabel.configure(anchor='center')
        # self.sportlabel.grid(column=0, row=3)

# Frame collecting CasparCG connection settings
        self.casparframe = ttk.Frame(self.appframe, padding='5')
        self.casparframe.grid(column=0, row=1)

        self.connectbutton = ttk.Button(self.casparframe, text="Connect", command=self.casparconnect)
        self.connectbutton.grid(column=0, row=0)
        self.disconnectbutton = ttk.Button(self.casparframe, text="Disconnect", command=self.caspardisconnect)
        self.disconnectbutton.grid(column=1, row=0)
        
        self.casparonline = StringVar()
        self.casparlabel = ttk.Label(self.casparframe, textvariable=self.casparonline).grid(column=0, row=1)

# Frame collecting serial port settings
        self.serialframe = ttk.Frame(self.appframe, padding='5')
        self.serialframe.grid(column=0, row=2)
        self.serialconnectbutton = ttk.Button(self.serialframe, text="Open Port", command=self.serialconnect)
        self.serialconnectbutton.grid(column=0, row=0)
        self.serialdisconnectbutton = ttk.Button(self.serialframe, text="Close Port", command=self.serialdisconnect)
        self.serialdisconnectbutton.grid(column=1, row=0)
        self.serialport = serial.Serial()
        self.serialport.baudrate = 9600
        
# Testing label
#         self.feedbackframe = ttk.Frame(self.appframe, padding='5')
#         self.feedbackframe.grid(column=0, row=3)
#         self.feedbacktext = StringVar()
#         self.feedbacklabel = ttk.Label(self.feedbackframe, textvariable=self.feedbacktext, width="80")
#         self.feedbacklabel.grid(column=0, row=0)
#         self.testbutton = ttk.Button(self.feedbackframe, text="Test", command=self.starttest)
#         self.testbutton.grid(column=0, row=1)
#         self.testrun = False

        # Instantiate score data objects
        self.homescore = CasparData(str(self.sportver))
        self.visitorscore = CasparData(str(self.sportver))
        self.clock = CasparData(str(self.sportver))
        self.shotclock = CasparData(str(self.sportver))
        self.homefouls = CasparData(str(self.sportver))
        self.visitorfouls = CasparData(str(self.sportver))
        self.period = CasparData(str(self.sportver))

    def casparconnect(self):
        try:
            # self.casparinst.connect()
            self.bbr0.state(['disabled'])
            self.bbr1.state(['disabled'])
            self.bbr2.state(['disabled'])
        except:
            raise IOError

    def caspardisconnect(self):
        try:
            # self.casparinst.disconnect()
            self.bbr0.state(['!disabled'])
            self.bbr1.state(['!disabled'])
            self.bbr2.state(['!disabled'])
        except:
            raise IOError

    def onlineindicator(self):
        pass
        
    def serialconnect(self):
        pass
        
    def serialdisconnect(self):
        pass
        
    def starttest(self):
        if self.testrun is False:
            self.testrun = True
        elif self.testrun is True:
            self.testrun = False


class CasparData(object):  # Base class for scoreboard data objects
    def __init__(self, ver):
        """
        :param ver:
        :attribute int parse_start: The start index for the desired field in the line
        :attribute int parse_stop: The stop index for same
        """
        self.ver = ver
        self.usedict = ''
        self.
        if self.ver == 'bbr0':
            self.usedict = 'bbr0dict'
        elif self.ver == 'bbr1':
            self.usedict = 'bbr1dict'
        elif self.ver == 'bbr2':
            self.usedict = 'bbr2dict'
        self.parse_start = self.usedict[self][0]
        self.parse_stop = self.usedict['str(self)'][1]
        # Constants of fields for input parsing
        bbr0dict = {
            'clock': [0, 7],
            'shotclock': [8, 10],
            'homescore': [11, 14],
            'visitorscore': [14, 17],
            'homefouls': [16, 18],
            'visitorfouls': [18, 20],
            'homefto': [20, 21],
            'homepto': [21, 22],
            'hometto': [22, 23],
            'visitorfto': [23, 24],
            'visitorpto': [24, 25],
            'visitortto': [25, 26],
            'period': [26, 27]
        }

        bbr1dict = {
            'clock': [0, 7],
            'shotclock': [8, 12],
            'homescore': [12, 15],
            'visitorscore': [15, 18],
            'homefouls': [18, 20],
            'visitorfouls': [20, 22],
            'homefto': [22, 23],
            'homepto': [23, 24],
            'hometto': [24, 25],
            'visitorfto': [25, 26],
            'visitorpto': [26, 27],
            'visitortto': [27, 28],
            'period': [28, 29]
        }

        bbr2dict = {
            'clock': [0, 7],
            'shotclock': [8, 12],
            'homescore': [12, 15],
            'visitorscore': [15, 18],
            'homefouls': [18, 20],
            'visitorfouls': [20, 22],
            'homefto': [22, 23],
            'homepto': [23, 24],
            'hometto': [24, 25],
            'visitorfto': [25, 26],
            'visitorpto': [26, 27],
            'visitortto': [27, 28],
            'period': [28, 29],
            'timeoutclock': [29, 34]
        }

    def parseinput(self, inputtext=' 8:00  s    0  0 0 0      156'):
        """
        :param str inputtext: The line of raw ASCII data received from serial

        """
        output = inputtext[self.parse_start:self.parse_stop].strip()
        return output

    def update_ver(self, value):
        self.ver.set(value)


# class HomeScore(CasparData):
#     if self.ver == 'Basketball Rev0':
#         parse_start = bbr0dict['homescore'][0]
#         parse_stop = bbr0dict['homescore'][1]
#     elif CasparData.ver == 'Basketball Rev1':
#         parse_start = bbr1dict['homescore'][0]
#         parse_stop = bbr1dict['homescore'][1]
#     elif CasparData.ver == 'Basketball Rev2':
#         parse_start = bbr2dict['homescore'][0]
#         parse_stop = bbr2dict['homescore'][1]
#     else:
#         raise ValueError
#
#
# class VisitorScore(CasparData):
#     if CasparData.ver == 'Basketball Rev0':
#         CasparData.parse_start = 14
#         CasparData.parse_stop = 17
#     elif CasparData.ver == 'Basketball Rev1':
#         CasparData.parse_start = 0
#         CasparData.parse_stop = 0
#     elif CasparData.ver == 'Basketball Rev2':
#         CasparData.parse_start = 0
#         CasparData.parse_stop = 0
#     else:
#         raise ValueError
#
#
# class Clock(CasparData):
#     if CasparData.ver == 'Basketball Rev0':
#         CasparData.parse_start = 0
#         CasparData.parse_stop = 7
#     elif CasparData.ver == 'Basketball Rev1':
#         CasparData.parse_start = 0
#         CasparData.parse_stop = 7
#     elif CasparData.ver == 'Basketball Rev2':
#         CasparData.parse_start = 0
#         CasparData.parse_stop = 7
#     else:
#         raise ValueError


root = Tk()
main = Scorer(root)
root.title("PyScore")
root.mainloop()
