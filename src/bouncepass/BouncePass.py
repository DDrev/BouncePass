# -*- coding: UTF-8 -*-

import caspartalk
import serial
import serial.tools.list_ports
from ParseTables import mastertable
import xml.etree.ElementTree as ETree
import copy


class Scorer(object):
    def __init__(self):
        self.globaldict = {}
        self.parsed_data = {}
        self.sport = self.sport_select()
        self.version = self.version_select()
        self.globaldict = self.assign_dict()
        self.serialport = serial.Serial(self.serial_select())
        self.parsed_data = self.data_setup()
        # self.casparinst = caspartalk.CasparServer(server_ip='127.0.0.1')
        self.casparinst = caspartalk.CasparServer(server_ip='192.168.1.108')
        # self.output = ''
        self.mainloop()

    @staticmethod
    def sport_select():
        sport_dict = {
            1: 'b',
            2: 'f',
            3: 'v'
        }
        print 'Enter sport:\n1 - Basketball\n2 - Football\n3 - Volleyball'
        sportentry = raw_input(">>>")
        if int(sportentry) in range(1, 4):
            return sport_dict[int(sportentry)]
        else:
            raise ValueError('Entry out of range')

    def version_select(self):
        version_dialog = {
            'b': 'Enter feed version:\n1 - Revision 0\n2 - Revision 1\n3 - Revision 2',
            'f': 'Enter feed version:\n1 - Revision 0\n2 - Revision 1',
        }
        if self.sport != 'v':
            print version_dialog[self.sport]
            versionentry = raw_input('>>>')
            return str(int(versionentry) - 1)
        elif self.sport == 'v':
            return '0'
        else:
            raise ValueError('Entry out of range')

    @staticmethod
    def serial_select():
        seriallist = serial.tools.list_ports.comports()
        print 'Enter serial port to use:'
        for i in range(len(seriallist)):
            print (i + 1), '-', seriallist[i]
        serialentry = raw_input('>>>')
        if int(serialentry) - 1 in range(len(seriallist)):
            return str(str(seriallist[int(serialentry) - 1]).partition(' - ')[0])
        else:
            raise ValueError('Entry out of range')

    def assign_dict(self):
        return mastertable[self.sport + 'br' + self.version + 'dict']

    def parse_serial(self):
        # new_data = self.serialport.read_all()
        new_data = ' 7:57       0  0 0 0      10E'
        self.serialport.flush()
        for key in self.parsed_data.iterkeys():
            self.parsed_data[key] = new_data[self.globaldict[key][0]:self.globaldict[key][1]]

    def data_setup(self):
        return dict.fromkeys(self.globaldict.iterkeys(), '0')

    def caspar_send(self, data):
        self.casparinst.send_amcp_command(amcp_command="CG 1-0 UPDATE 1 \"{0}\"".format(self.format_output(data)))

    @staticmethod
    def format_output(output_dict):
        output_string = ''
        output_string += '<templateData>'
        for key, value in output_dict.iteritems():
            data_string = ''
            data_string += '<componentData id=\"{0}\">'.format(key)
            data_string += '<data id=\"text\" value=\"{0}\" /></componentData>'.format(value)
            output_string += data_string
        # for i in range(:10000):
        #     data_string = ''
        #     data_string += '<componentData id=\"f0\">'
        #     data_string += '<data id=\"text\" value=\"{0}\" /></componentData>'.format(i)
        #     output_string += data_string
        output_string += '</templateData>'
        return output_string

    def mainloop(self):
        while 1:
            self.parse_serial()
            self.caspar_send(self.parsed_data)


# class CasparData(object):  # Base class for scoreboard data objects
#     def __init__(self, ident, start, stop):
#         """
#         :rtype : object
#         :param ident: The score data item contained by this object
#         :param start: The start position for parsing input string from serial
#         :param stop: The stop position for parsing input string from serial
#         """
#         self.ident = ident
#         self.field = ''  # Field in Flash template this object's data will be displayed in
#         self.value = ''  # Contents of data object
#         self.start = start
#         self.stop = stop

    # def set_params(self):
    #     self.start = mastertable[self.globaldict, self.ident, 0]
    #     self.stop = mastertable[self.globaldict, self.ident, 1]

    # def parse_input(self, input_string):
    #     with input_string as i:
    #         new_value = i[self.start, self.stop]
    #         return new_value
