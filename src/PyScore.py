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
        
        self.casparinst = caspartalk.CasparServer()

# Subframe collecting sport and TV feed version settings
        self.sportframe = ttk.Frame(self.appframe, padding='5')
        self.sportframe.grid(column=0, row=0)
        
        self.sportver = StringVar()

        self.sportmenu = ttk.Combobox(self.sportframe, textvariable=self.sportver)
        self.sportmenu['values'] = ('Basketball Rev0', 'Basketball Rev1', 'Basketball Rev2')
        self.sportver = 'Basketball Rev0'
        self.sportmenu.grid(column=0, row=0)
        self.sportmenu.bind('<<ComboboxSelected>>', self.sportmenu.selection_clear())
        self.sportmenu.state(['readonly'])
        self.sportlabel = ttk.Label(self.sportframe, textvariable=self.sportver)
        self.sportlabel.configure(anchor='center')
        self.sportlabel.grid(column=0, row=1)

# Subframe collecting CasparCG connection settings
        self.casparframe = ttk.Frame(self.appframe, padding='5')
        self.casparframe.grid(column=0, row=1)

        self.connectbutton = ttk.Button(self.casparframe, text="Connect", command=self.casparconnect)
        self.connectbutton.grid(column=0, row=0)
        self.disconnectbutton = ttk.Button(self.casparframe, text="Disconnect", command=self.caspardisconnect)
        self.disconnectbutton.grid(column=1, row=0)
        
        self.casparonline = StringVar()
        self.casparlabel = ttk.Label(self.casparframe, textvariable=self.casparonline).grid(column=0, row=1)

# Subframe collecting serial port settings
        self.serialframe = ttk.Frame(self.appframe, padding='5')
        self.serialframe.grid(column=0, row=2)
        self.serialconnectbutton = ttk.Button(self.serialframe, text="Open Port", command=self.serialconnect)
        self.serialconnectbutton.grid(column=0, row=0)
        self.serialdisconnectbutton = ttk.Button(self.serialframe, text="Close Port", command=self.serialdisconnect)
        self.serialdisconnectbutton.grid(column=1, row=0)
        self.serialport = serial.Serial()
        self.serialport.baudrate = 9600
        
# Testing label
        self.feedbackframe = ttk.Frame(self.appframe, padding='5')
        self.feedbackframe.grid(column=0, row=3)
        self.feedbacktext = StringVar()
        self.feedbacklabel = ttk.Label(self.feedbackframe, textvariable=self.feedbacktext, width="80")
        self.feedbacklabel.grid(column=0, row=0)
        self.testbutton = ttk.Button(self.feedbackframe, text="Test", command=self.starttest)
        self.testbutton.grid(column=0, row=1)
        self.testrun = False

    def casparconnect(self):
        try:
            self.casparinst.connect()
            self.sportmenu.state(['disabled'])
        except:
            raise IOError

    def caspardisconnect(self):
        self.casparinst.disconnect()
        self.sportmenu.state(['readonly'])

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
    def __init__(self, inputtext, ver):
        self.inputtext = inputtext
        self.ver = ver
        self.parse_start = 0
        self.parse_stop = 0
        # Breakdown of fields for input parsing
        self.bbr0dict = {
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

        self.bbr0dict = {
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

        self.bbr0dict = {
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

    def parseinput(self, inputtext, parse_start, parse_stop):
        """
        :param str inputtext: The line of raw ASCII data received from serial
        :param int parse_start: The start index for the desired field in the line
        :param int parse_stop: The stop index for same
        """
        output = inputtext[parse_start:parse_stop].strip()
        return output


class HomeScore(CasparData):
    if CasparData.ver == 'Basketball Rev0':
        parse_start = CasparData.bbr0dict['homescore'][0]
        parse_stop = CasparData.bbr0dict['homescore'][1]
    elif CasparData.ver == 'Basketball Rev1':
        parse_start = CasparData.bbr1dict['homescore'][0]
        parse_stop = CasparData.bbr1dict['homescore'][1]
    elif CasparData.ver == 'Basketball Rev2':
        parse_start = CasparData.bbr2dict['homescore'][0]
        parse_stop = CasparData.bbr2dict['homescore'][1]
    else:
        raise ValueError
            

class VisitorScore(CasparData):
    if CasparData.ver == 'Basketball Rev0':
        CasparData.parse_start = 14
        CasparData.parse_stop = 17
    elif CasparData.ver == 'Basketball Rev1':
        CasparData.parse_start = 0
        CasparData.parse_stop = 0
    elif CasparData.ver == 'Basketball Rev2':
        CasparData.parse_start = 0
        CasparData.parse_stop = 0
    else:
        raise ValueError
            

class Clock(CasparData):
    if CasparData.ver == 'Basketball Rev0':
        CasparData.parse_start = 0
        CasparData.parse_stop = 7
    elif CasparData.ver == 'Basketball Rev1':
        CasparData.parse_start = 0
        CasparData.parse_stop = 7
    elif CasparData.ver == 'Basketball Rev2':
        CasparData.parse_start = 0
        CasparData.parse_stop = 7
    else:
        raise ValueError


root = Tk()
main = Scorer(root)
root.title("PyScore")
root.mainloop()
