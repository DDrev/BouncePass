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
        self.globaldict = {}
        self.startup()
        self.serialport = serial.Serial

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

    def assigndict(self):
        if self.sport is 0 and self.version is 0:
            self.globaldict = mastertable['bbr0dict']
        elif self.sport is 0 and self.version is 1:
            self.globaldict = mastertable['bbr1dict']
        elif self.sport is 0 and self.version is 2:
            self.globaldict = mastertable['bbr2dict']
        elif self.sport is 1 and self.version is 0:
            self.globaldict = mastertable['fbr0dict']
        elif self.sport is 1 and self.version is 1:
            self.globaldict = mastertable['fbr1dict']
        elif self.sport is 2:
            self.globaldict = mastertable['vbr0dict']
        else:
            raise ValueError

    def startup(self):
        # Startup dialog asking for sport, version, and serial port to use
        self.sportselect()
        self.versionselect()
        self.serialselect()
        self.assigndict()
        self.inst_general_objects()
        if self.sport is 0:
            self.inst_bb_objects()
        elif self.sport is 1:
            self.inst_fb_objects()
        elif self.sport is 2:
            self.inst_vb_objects()

    def start_lookup(self, ident):
        pass

    def stop_lookup(self, ident):
        pass

    def inst_general_objects(self):
        # Instantiate score data objects used in all sports
        general_list = ['homescore', 'visitorscore', 'clock', 'period', 'hometto', 'visitortto']
        for i in general_list:
          = CasparData(i, self.globaldict[i, 0], self.globaldict[i, 1])
        # self.homescore = CasparData('homescore', start_lookup('homescore'))
        # self.visitorscore = CasparData('visitorscore', self.globaldict)
        # self.clock = CasparData('clock', self.globaldict)
        # self.period = CasparData('period', self.globaldict)
        # self.hometto = CasparData('hometto', self.globaldict)
        # self.visitortto = CasparData('visitortto', self.globaldict)

    def inst_bb_objects(self):  # Instantiate basketball specific data objects
        self.homefouls = CasparData('homefouls', self.globaldict)
        self.visitorfouls = CasparData('visitorfouls', self.globaldict)
        self.shotclock = CasparData('shotclock', self.globaldict)
        self.homepto = CasparData('homepto', self.globaldict)
        self.visitorpto = CasparData('visitorpto', self.globaldict)
        self.homefto = CasparData('homefto', self.globaldict)
        self.visitorfto = CasparData('visitorfto', self.globaldict)

    def inst_fb_objects(self):  # Instantiate football specific data objects
        self.ballon = CasparData('ballon', self.globaldict)
        self.down = CasparData('down', self.globaldict)
        self.playclock = CasparData('playclock', self.globaldict)

    def inst_vb_objects(self):  # Instantiate volleyball specific data objects
        self.homewins = CasparData('homewins', self.globaldict)
        self.visitorwins = CasparData('visitorwins', self.globaldict)
        self.gamenumber = CasparData('gamenumber', self.globaldict)

    def caspar_connect(self):
        # casparinst = caspartalk.CasparServer
        pass


class CasparData(object):  # Base class for scoreboard data objects
    def __init__(self, ident, start, stop):
        """
        :rtype : object
        :param ident: The score data item contained by this object
        :param start: The start position for parsing input string from serial
        :param stop: The stop position for parsing input string from serial
        """
        self.ident = ident
        self.field = ''  # Field in Flash template this object's data will be displayed in
        self.value = ''  # Contents of data object
        self.start = start
        self.stop = stop

    def set_params(self):
        self.start = mastertable[self.globaldict, self.ident, 0]
        self.stop = mastertable[self.globaldict, self.ident, 1]

    def parse_input(self, input_string):
        with input_string as i:
            new_value = i[self.start, self.stop]
            return new_value
