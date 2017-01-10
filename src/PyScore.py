# -*- coding: UTF-8 -*-

from Tkinter import *
import ttk
import serial
import caspartalk
import socket


class Scorer(object):
    def __init__(self, parent):
        """

        :type parent: object
        """
        self.parent = parent

# Main containing frame
        self.appframe = ttk.Frame(parent, padding="5")
        self.appframe.grid(column=0, row=0)
        
        self.target_text = "capture.txt"  # Variable for file for testing text parsing
        self.raw_text = open(self.target_text, 'r') # Also for test purposes
        self.casparinst = CasparInstance()

# Subframe collecting sport and TV feed version settings
        self.sportframe = ttk.Frame(self.appframe, padding='5')
        self.sportframe.grid(column=0, row=0)
        
        self.sportver = StringVar()

        self.sportmenu = ttk.Combobox(self.sportframe, textvariable=self.sportver)
        self.sportmenu['values'] = ('Basketball Rev0', 
            'Basketball Rev1', 'Basketball Rev2')
        sportver = 'Basketball Rev0'
        self.sportmenu.grid(column=0, row=0)
        self.sportmenu.bind('<<ComboboxSelected>>', self.sportmenu.selection_clear() )
        self.sportmenu.state(['readonly'])
        self.sportlabel = ttk.Label(self.sportframe, textvariable=self.sportver)
        self.sportlabel.configure(anchor = 'center')
        self.sportlabel.grid(column=0, row=1)

# Subframe collecting CasparCG connection settings
        self.casparframe = ttk.Frame(self.appframe, padding='5')
        self.casparframe.grid(column=0, row=1)

        self.connectbutton = ttk.Button(self.casparframe, text="Connect", 
            command = self.casparconnect)
        self.connectbutton.grid(column=0, row=0)
        self.disconnectbutton = ttk.Button(self.casparframe, text="Disconnect",
            command=self.caspardisconnect)
        self.disconnectbutton.grid(column=1, row=0)
        
        self.casparonline = StringVar()
        self.casparlabel = ttk.Label(self.casparframe, \
            textvariable=self.casparonline).grid(column=0, row=1)

# Subframe collecting serial port settings
        self.serialframe = ttk.Frame(self.appframe, padding='5')
        self.serialframe.grid(column=0, row=2)
        self.serialconnectbutton = ttk.Button(self.serialframe, text="Open Port", \
        command=self.serialconnect )
        self.serialconnectbutton.grid(column=0, row=0)
        self.serialdisconnectbutton = ttk.Button(self.serialframe, text="Close Port", \
        command=self.serialdisconnect )
        self.serialdisconnectbutton.grid(column=1, row=0)
        self.serialport = serial.Serial()
        self.serialport.baudrate = 9600
        
# Testing label
        self.feedbackframe = ttk.Frame(self.appframe, padding='5')
        self.feedbackframe.grid(column=0, row=3)
        self.feedbacktext = StringVar()
        self.feedbacklabel = ttk.Label(self.feedbackframe, \
            textvariable=self.feedbacktext, width="80")
        self.feedbacklabel.grid(column=0, row=0)
        self.testbutton = ttk.Button(self.feedbackframe, text="Test", \
        command=self.starttest )
        self.testbutton.grid(column=0, row=1)
        self.testrun = False
        
        self.work = file.readline(self.raw_text)
        self.homescore = HomeScore(self.work)
        self.visitorscore = VisitorScore(self.work, self.sportver)
        self.clock = Clock(self.work, self.sportver)

        while self.testrun == True:
            self.homescore.parseinput(work)
            self.visitorscore.parseinput(work)
            self.clock.parseinput(work)
            self.feedbacktext.set(self.homescore + self.visitorscore + self.clock)




    def casparconnect(self):
        self.casparinst.connect()
        self.sportmenu.state(['disabled'])


    def caspardisconnect(self):
         self.casparinst.disconnect()
         self.sportmenu.state(['readonly'])

    def onlineindicator():
        pass
        
    def serialconnect(self):
        pass
        
    def serialdisconnect(self):
        pass
        
    def starttest(self):
        if self.testrun == False:
            self.testrun = True
        elif self.testrun == True:
            self.testrun = False
            
            
        
    
        

        
#     def home_score_slice(n):
#       score = n[11:14]
#       score = score.strip()
#       return score
# 
#     def clock_slice(n):
#       clock = n[0:7]
#       clock = clock.strip()
#       return clock
# 
#     def visitor_score_slice(n):
#       score = n[14:17]
#       score = score.strip()
#       return score
        

# Main object representing CasparCG server
# Overrides auto connection on instantiation
class CasparInstance(caspartalk.CasparServer):
    def __init__(self):
        self.buffer_size = 4096
        self.server_ip = '127.0.0.1'
        self.server_port = 5250
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        super(CasparInstance, self).connect()

    def disconnect(self):
        super(CasparInstance, self).disconnect()
        
class CasparData(object):  # Base class for scoreboard data objects
    def __init__(self, input):
        self.input = input
        self.parse_start = 0
        self.parse_stop = 0
    def parseinput(input, parse_start, parse_stop):
        output = input[parse_start:parse_stop].strip()
        return output
# Breakdown of fields for input parsing
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
    
        

class HomeScore(CasparData):
    def __init__(self, input):
        self.input = input
        if main.sportver == 'Basketball Rev0':
            self.parse_start = self.bbr0dict['homescore'][0]
            self.parse_stop = self.bbr0dict['homescore'][1]
        elif ver == 'Basketball Rev1':
            self.parse_start = self.bbr1dict['homescore'][0]
            self.parse_stop = self.bbr1dict['homescore'][1]
        elif ver == 'Basketball Rev2':
            self.parse_start = self.bbr2dict['homescore'][0]
            self.parse_stop = self.bbr2dict['homescore'][1]
        else:
            raise ValueError
            
class VisitorScore(CasparData):
    def __init__(self, input, ver):
        self.input = input
        self.ver = ver
        if self.ver == 'Basketball Rev0':
            self.parse_start = 14
            self.parse_stop = 17
        elif self.ver == 'Basketball Rev1':
            self.parse_start = 0
            self.parse_stop = 0
        elif self.ver == 'Basketball Rev2':
            self.parse_start = 0
            self.parse_stop = 0
        else:
            raise ValueError
            
class Clock(CasparData):
    def __init__(self, input, ver):
        self.input = input
        self.ver = ver
        if self.ver == 'Basketball Rev0':
            self.parse_start = 0
            self.parse_stop = 7
        elif self.ver == 'Basketball Rev1':
            self.parse_start = 0
            self.parse_stop = 7
        elif self.ver == 'Basketball Rev2':
            self.parse_start = 0
            self.parse_stop = 7
        else:
            raise ValueError
        


#     def main_loop(file):
#       for line in file:
#           home_score = home_score_slice(line)
#           clock = clock_slice(line)
#           visitor_score = visitor_score_slice(line)
#           print clock, home_score, visitor_score
    

root = Tk()
main = Scorer(root)
root.title("PyScore")
root.mainloop()


