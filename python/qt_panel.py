#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
import pmt
from gnuradio import gr
from PyQt4 import Qt, QtCore, QtGui

from rds_const import callsign

class Indicator(QtGui.QLabel):

    def __init__(self, label, parent = None):
        super(Indicator, self).__init__(parent)

        self.setText(label)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFrameStyle(QtGui.QFrame.Raised | QtGui.QFrame.StyledPanel)

        self.stylesheet_true = "QLabel { background-color : green; color : white; }"
        self.stylesheet_false = "QLabel { background-color : grey; color : white; }"

        self.setStatus(False)

    def setStatus(self, status):
        if status:
            self._stylesheet = self.stylesheet_true
        else:
            self._stylesheet = self.stylesheet_false

    def paintEvent(self, event):
        self.setStyleSheet(self._stylesheet)
        QtGui.QLabel.paintEvent(self, event)

class RdsFlagPanel(QtGui.QWidget):

    def __init__(self, parent = None):
        super(RdsFlagPanel, self).__init__(parent)

        self.initUI()
        self.reset()

    def initUI(self):

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        self.traffic_program = Indicator('Traffic Program')
        self.grid.addWidget(self.traffic_program, 0, 0)

        self.traffic_alert = Indicator('Traffic Alert')
        self.grid.addWidget(self.traffic_alert, 0, 1)

        self.filler_0_2 = Indicator('')
        self.grid.addWidget(self.filler_0_2, 0, 2)

        self.filler_0_3 = Indicator('')
        self.grid.addWidget(self.filler_0_3, 0, 3)

        self.music = Indicator('Music')
        self.grid.addWidget(self.music, 1, 0)

        self.speech = Indicator('Speech')
        self.grid.addWidget(self.speech, 1, 1)

        self.stereo = Indicator('Stereo')
        self.grid.addWidget(self.stereo, 1, 2)

        self.mono = Indicator('Mono')
        self.grid.addWidget(self.mono, 1, 3)

        self.artificial_head = Indicator('Artificial Head')
        self.grid.addWidget(self.artificial_head, 2, 0)

        self.compressed = Indicator('Compressed')
        self.grid.addWidget(self.compressed, 2, 1)

        self.dynamic_pty = Indicator('Dynamic PTY')
        self.grid.addWidget(self.dynamic_pty, 2, 2)

        self.filler_2_3 = Indicator('')
        self.grid.addWidget(self.filler_2_3, 2, 3)

        self.setLayout(self.grid)

    def reset(self):
        self.traffic_program.setStatus(False)
        self.traffic_alert.setStatus(False)
        self.music.setStatus(False)
        self.speech.setStatus(False)
        self.stereo.setStatus(False)
        self.mono.setStatus(False)
        self.artificial_head.setStatus(False)
        self.compressed.setStatus(False)
        self.dynamic_pty.setStatus(False)

    def update(self, flags):
        flags = [flag == '1' for flag in flags]
        self.traffic_program.setStatus(flags[0])
        self.traffic_alert.setStatus(flags[1])
        self.music.setStatus(flags[2])
        self.speech.setStatus(not flags[2])
        self.stereo.setStatus(not flags[3])
        self.mono.setStatus(flags[3])
        self.artificial_head.setStatus(flags[4])
        self.compressed.setStatus(flags[5])
        self.dynamic_pty.setStatus(flags[6])

class qt_panel(gr.sync_block, QtGui.QWidget):
    '''
    Panel for the display of RDS information in Qt GUI
    '''

    def __init__(self):
        gr.sync_block.__init__(self, 'rds_qtpanel',[],[])
        QtGui.QWidget.__init__(self)
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handler)
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()

        self.monofont = QtGui.QFont('Courier')
        self.program_info = Qt.QLabel('')
        self.program_info_label = QtGui.QLabel('Station Callsign:')
        self.program_info.setFont(self.monofont)
        self.program_info.setStyleSheet("QLabel { background-color : black; color : white; }")

        self.radio_text = Qt.QLabel('')
        self.radio_text_label = QtGui.QLabel('Radio Text:')
        self.radio_text.setFont(self.monofont)
        self.radio_text.setStyleSheet("QLabel { background-color : black; color : white; }")

        self.station_name = Qt.QLabel('')
        self.station_name_label = QtGui.QLabel('Station Name:')
        self.station_name.setFont(self.monofont)
        self.station_name.setStyleSheet("QLabel { background-color : black; color : white; }")
        self.flags = RdsFlagPanel()

        self.grid.addWidget(self.program_info_label, 0, 0)
        self.grid.addWidget(self.program_info, 0, 1)
        self.grid.addWidget(self.radio_text_label, 2, 0)
        self.grid.addWidget(self.radio_text, 2, 1)
        self.grid.addWidget(self.station_name_label, 1, 0)
        self.grid.addWidget(self.station_name, 1, 1)
        self.grid.addWidget(self.flags, 0, 2, 3, 2)

        self.setLayout(self.grid)

    def handler(self, rds_data):
        msg_type = pmt.to_long(pmt.tuple_ref(rds_data, 0))
        msg = pmt.symbol_to_string(pmt.tuple_ref(rds_data, 1))
        if msg_type == 4:
            self.radio_text.setText(msg.strip())
        elif msg_type == 1:
            self.station_name.setText(msg)
        elif msg_type == 0:
            self.program_info.setText(callsign(msg))
        elif msg_type == 3:
            self.flags.update(msg)

    def set_frequency(self, frequency):
        '''
        frequency param change callback
        '''
        self.radio_text.setText('')
        self.station_name.setText('')
        self.program_info.setText('')
        self.flags.reset()


    def work(self, input_items, output_items):
        pass
