# -*- coding: UTF-8 -*-

import caspartalk
import serial
import serial.tools.list_ports
from ParseTables import mastertable
import copy
import time


class Scorer(object):
    def __init__(self):
        self.globaldict = {}
        self.parsed_data = {}
        self.output_data = {}
        self.sport = self.sport_select()
        self.version = self.version_select()
        self.globaldict = self.assign_dict()
        self.serial_port = serial.Serial(self.serial_select(), baudrate=9600, timeout=2)
        self.parsed_data = self.data_setup()
        self.cached_data = copy.deepcopy(self.parsed_data)
        self.casparinst = caspartalk.CasparServer(server_ip='127.0.0.1')
        # self.casparinst = caspartalk.CasparServer(server_ip='192.168.1.108')
        # self.testinput = file('capture.txt')
        self.serial_port.reset_input_buffer()
        self.mainloop()

    def sport_select(self):
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

    def serial_select(self):
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

    def get_serial(self):
        data_string = ''
        while True:
            byte_read = self.serial_port.read(1)
            if byte_read == '\x01':
                break
        while True:
            byte_read = self.serial_port.read(1)
            if byte_read == '\x04':
                break
            else:
                data_string += byte_read
        return data_string

    def parse_serial(self, data_string):
        new_data = data_string
        # new_data = ' 7:57       0  0 0 0      10E'
        # new_data = self.testinput.readline()
        self.output_data = {}
        for key in self.parsed_data.iterkeys():
            self.parsed_data[key] = new_data[self.globaldict[key][0]:self.globaldict[key][1]]
            if key != 'checksum':
                if self.parsed_data[key] != self.cached_data[key]:
                    self.output_data[key] = self.parsed_data[key]
            self.cached_data[key] = self.parsed_data[key]

    def data_setup(self):
        return dict.fromkeys(self.globaldict.iterkeys(), '0')

    def caspar_send(self, data):
        if data != {}:
            self.casparinst.send_amcp_command(amcp_command='CG 1-1 UPDATE 1 \"{0}\"'.format(self.format_output(data)))
            # print 'CG 1-0 UPDATE 1 \"{0}\"'.format(self.format_output(data))
        else:
            pass

    def format_output(self, output_dict):
        output_string = ''
        output_string += '<templateData>'
        for key, value in output_dict.iteritems():
            output_string += '<componentData id=\\\"{0}\\\"><data id=\\\"text\\\" value=\\\"{1}\\\" /></componentData>'\
                .format(key, value)
        output_string += '</templateData>'
        return output_string

    def mainloop(self):
        while 1:
            # print self.get_serial()
            self.parse_serial(self.get_serial())
            self.caspar_send(self.output_data)
            # time.sleep(0.05)

    def exit_close_serial(self):
        self.serial_port.close()
