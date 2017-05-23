# -*- coding: UTF-8 -*-

import caspartalk
import serial
import serial.tools.list_ports


class Scorer(object):
    def __init__(self):
        self.sport = 0
        self.version = 0
        self.serial = 0
        self.startup()

    class CasparData(object):  # Base class for scoreboard data objects
        def __init__(self, ident):
            """
            :rtype : object
            :param ident: The score data item contained by this object
            """
            self.ident = ident
            self.field = ''  # Field in Flash template this object's data will be displayed in
            self.value = ''  # Contents of data object

        @classmethod
        def parseinput(self):
            pass

    def sportselect(self):
        with raw_input('Enter sport:\n1 - Basketball\n2 - Football\n3 - Volleyball') as entry:
            try:
                if int(entry) in range(1, 4):
                    self.sport = entry - 1
            except:
                raise ValueError

    def versionselect(self):
        if self.sport is 0:
            with raw_input('Enter feed version:\n1 - Revision 0\n2 - Revision 1\n3 - Revision 2') as entry:
                self.version = int(entry) - 1
        elif self.sport is 1:
            with raw_input('Enter feed version:\n 1 - Revision 0\n 2 - Revision 1') as entry:
                self.version = int(entry) - 1
        elif self.sport is 2:
            self.version = 0
        else:
            raise ValueError

    def startup(self):
        # Startup dialog asking for sport, version, and serial port to use
        self.sportselect()
        self.versionselect()
        self.serialselect()
        self.instobjects()

    def serialselect(self):
        seriallist = serial.tools.list_ports.comports()
        for i in range(len(seriallist)):
            print (i + 1), '-', seriallist[i]
        with raw_input('Enter serial port to use:') as entry:
            self.serial = int(entry) - 1

    def instobjects(self):
        # Instantiate score data objects
        homescore = self.CasparData('homescore')
        visitorscore = self.CasparData('visitorscore')
        clock = self.CasparData('clock')
        period = self.CasparData('period')
        shotclock = self.CasparData('shotclock')
        homefouls = self.CasparData('homefouls')
        visitorfouls = self.CasparData('visitorfouls')

    def casparconnect(self):
        # casparinst = caspartalk.CasparServer
        pass

    def instserial(self):  # Instantiate object and open serial port
        serialport = serial.Serial



