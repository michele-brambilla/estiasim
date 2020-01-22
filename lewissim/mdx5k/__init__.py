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

from lewis.adapters.epics import PV, EpicsInterface
from lewis.core import approaches
from lewis.core.statemachine import State
from lewis.core.utils import check_limits
from lewis.devices import StateMachineDevice


class OnState(State):
    def in_state(self, dt):
        self._context.status = 'on'


class OffState(State):
    def in_state(self, dt):
        self._context.status = 'off'


class SimulatedMDX5K(StateMachineDevice):
    speed = 1.0
    modes = { 4: 'power', 5: 'current', 6: 'voltage' }

    def _initialize_data(self):
        self.status = 'off'
        self.interlock = ''
        self._status_command = 0
        self._value = 0.0
        self.voltage = 0.0
        self.current = 0.0
        self.power = 0.0
        self._target = 0.0

    def _get_state_handlers(self):
        return {
            'off': OffState(),
            'on': OnState(),
        }

    def _get_initial_state(self):
        return 'off'

    def _get_transition_handlers(self):
        return OrderedDict([
                (('off', 'on'), lambda: self._status_command == 1),
                (('on', 'off'), lambda: self._status_command == 0),
 ])

    @property
    def status_command(self):
        return self._status_command

    @status_command.setter
    def status_command(self, value):
        if value in [2,3]:
            return
        self._status_command = value
        if value > 1:
            if self.status == 1:
                print('Switch to new mode forbidden if power is on')
                return
            for mode, name in self.modes.items():
                setattr(self, name, True if mode == value else False)


    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def value(self):
        return self._value


class MDX5KEpicsInterface(EpicsInterface):
    """
    Motor EPICS interface
    """
    pvs = {

        'Status': PV('status', read_only=True, doc='Power supply status.', type='string'),
        'Interlock': PV('interlock', doc='Locked value.', type='string'),
        'StatusCommand': PV('status_command', doc='Command to switch status',
                            type='int'),
        'OutputSetpoint-RBV': PV('value', read_only=True,
                   doc='Readback value for the setpoint.'),
        'OutputSetpoint': PV('target', doc='Target value.'),
        'Voltage': PV('voltage', doc='Actual voltage.', unit='V',
                      read_only=True),
        'Current': PV('current', doc='Actual current.', unit='A',
                      read_only=True),
        'Power': PV('power', doc='Actual power.', unit='W', read_only=True),

    }

    _commands = {'start': 'start',
                 'stop': 'stop',
                 }

    _last_command = ''

    @property
    def execute_command(self):
        """
        Command to execute. Possible commands are start, stop.
        """
        return ''

    @execute_command.setter
    def execute_command(self, value):
        command = self._commands.get(value)

        getattr(self.device, command)()
        self._last_command = command

    @property
    def last_command(self):
        """
        The last command that was executed successfully.
        """
        return self._last_command


# setups = dict(
#     moving=dict(
#         device_type=SimulatedMDX5K,
#         parameters=dict(
#             override_initial_state='moving',
#             override_initial_data=dict(
#                 _target=0.0, _position=20.0
#             )
#         )
#     )
# )

framework_version = '1.2.1'
