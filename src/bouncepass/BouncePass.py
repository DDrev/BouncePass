# -*- coding: UTF-8 -*-

import caspartalk
import serial
import serial.tools.list_ports
from ParseTables import mastertable


class Scorer(object):
    def __init__(self):
        self.sport = 0
        self.version = 0
        self.serial = 0
        self.startup()

    class EntryError(ValueError):
        pass

    class CasparData(object):  # Base class for scoreboard data objects
        def __init__(self, ident):
            """
            :rtype : object
            :param ident: The score data item contained by this object
            """
            self.ident = ident
            self.field = ''  # Field in Flash template this object's data will be displayed in
            self.value = ''  # Contents of data object
            self.start = 0
            self.stop = 0

        @classmethod
        def parseinput(cls):
            pass

    def sportselect(self):
        print 'Enter sport:\n1 - Basketball\n2 - Football\n3 - Volleyball'
        sportentry = int(raw_input('>>>'))
        try:
            if int(sportentry) in range(1, 4):
                self.sport = sportentry - 1
        except:
            raise ValueError

    def versionselect(self):
        if self.sport is 0:
            print 'Enter feed version:\n1 - Revision 0\n2 - Revision 1\n3 - Revision 2'
            versionentry = raw_input('>>>')
            self.version = int(versionentry) - 1
        elif self.sport is 1:
            print 'Enter feed version:\n1 - Revision 0\n2 - Revision 1'
            versionentry = raw_input('>>>')
            self.version = int(versionentry) - 1
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
        print 'Enter serial port to use:'
        for i in range(len(seriallist)):
            print (i + 1), '-', seriallist[i]
        serialentry = raw_input('>>>')
        if int(serialentry) - 1 in range(len(seriallist)):
            self.serial = int(serialentry) - 1
        else:
            raise ValueError

    def instgeneralobjects(self):
        # Instantiate score data objects used in all sports
        self.homescore = self.CasparData('homescore')
        self.visitorscore = self.CasparData('visitorscore')
        self.clock = self.CasparData('clock')
        self.period = self.CasparData('period')
        self.hometto = self.CasparData('hometto')
        self.visitortto = self.CasparData('visitortto')

    def instbbobjects(self):  # Instantiate basketball specific data objects
        self.homefouls = self.CasparData('homefouls')
        self.visitorfouls = self.CasparData('visitorfouls')
        self.shotclock = self.CasparData('shotclock')
        self.homepto = self.CasparData('homepto')
        self.visitorpto = self.CasparData('visitorpto')
        self.homefto = self.CasparData('homefto')
        self.visitorfto = self.CasparData('visitorfto')

    def instfbobjects(self):  # Instantiate football specific data objects
        self.ballon = self.CasparData('ballon')
        self.down = self.CasparData('down')
        self.playclock = self.CasparData('playclock')

    def casparconnect(self):
        # casparinst = caspartalk.CasparServer
        pass

    def instserial(self):  # Instantiate object and open serial port
        serialport = serial.Serial



