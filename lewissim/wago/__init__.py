# -*- coding: utf-8 -*-
# *********************************************************************
# lewis - a library for creating hardware device simulators
# Copyright (C) 2016-2017 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************
import math
from collections import OrderedDict

from lewis.adapters.stream import StreamInterface, Cmd, scanf, Var
from lewis.core.statemachine import State
from lewis.core.utils import check_limits
from lewis.devices import StateMachineDevice, Device


class WagoSimulatedDevice(Device):
    param = 10

    def __init__(self, *args, **kwargs):
        super(WagoSimulatedDevice, self).__init__()
        self.values = [0 for _ in range(16)]

    def say_world(self):
        return "world!"

    def say_bar(self):
        return "bar!"

    def say_what(self, what):
        channel = what[0]
        value = what[1]
        print(channel)
        print(value)


class WagoInterface(StreamInterface):
    """
    A simple device where commands are terminated by a timeout.
    This demonstrates how to implement devices that do not have standard
    terminators and where a command is considered terminated after a certain
    time delay of not receiving more data.
    To interact with this device, you must switch telnet into char mode, or use
    netcat with special tty settings:
        $ telnet host port
        ^]
        telnet> mode char
        [type command and wait]
        $ stty -icanon && nc host port
        hello world!
        foobar!
    The following commands are available:
     - ``hello ``: Reply with "world!"
     - ``foo``: Replay with "bar!"
     - ``P``: Returns the device parameter
     - ``P=something``: Set parameter to specified value
    """
    commands = {
        # Space as \x20 represents a custom 'terminator' for this command only
        # However, waiting for the timeout still applies
        Cmd('say_world', pattern=scanf('hello\x20')),
        Cmd('say_bar', pattern=scanf('foo\x20')),
        Cmd('say_what', pattern='\x00\x00\x00\x00\x00\x06\x00\x05\x00(.*)',argument_mappings=[bytes]),
        Var('param', read_pattern=scanf('P'), write_pattern=scanf('P=%d')),
    }

    # An empty in_terminator triggers "timeout mode"
    # Otherwise, a ReadTimeout is considered an error.
    in_terminator = ''
    out_terminator = '\r\n'

    # Unusually long, for easier manual entry
    readtimeout = 2500

    def handle_error(self, request, error):
        return 'An error occurred: ' + repr(error)
