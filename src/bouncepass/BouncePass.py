# -*- coding: UTF-8 -*-

from Tkinter import *

import caspartalk


class Scorer(object):
    def __init__(self):
        # Instantiate score data objects
        self.homescore = CasparData()
        self.visitorscore = CasparData()
        self.clock = CasparData()
        self.period = CasparData()

        self.shotclock = CasparData()
        self.homefouls = CasparData()
        self.visitorfouls = CasparData()

    def casparconnect(self):
        casparinst = caspartalk.CasparServer
        pass
        
    def serialconnect(self):
        pass


class CasparData(object):  # Base class for scoreboard data objects
    def __init__(self, ver):
        """
        :param ver: The sport and feed version
        :attribute int parse_start: The start index for the desired field in the line
        :attribute int parse_stop: The stop index for same
        """
        self.ver = ver
        self.usedict = ''
        if self.ver == 'bbr0':
            self.usedict = 'bbr0dict'
        elif self.ver == 'bbr1':
            self.usedict = 'bbr1dict'
        elif self.ver == 'bbr2':
            self.usedict = 'bbr2dict'
        self.parse_start = self.usedict['str(self)'][0]
        self.parse_stop = self.usedict['str(self)'][1]
        # Constants of fields for input parsing

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
