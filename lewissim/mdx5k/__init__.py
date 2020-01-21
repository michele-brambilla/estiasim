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


class DefaultMovingState(State):
    def __init__(self, parameter):
        super(DefaultMovingState, self).__init__()
        self._parameter = parameter

    def in_state(self, dt):
        old = self._context.value
        self._context._value = approaches.linear(old,
                                                getattr(self._context,
                                                        self._parameter),
                                                self._context._speed, dt)

        self.log.info('Moved position (%s -> %s), target=%s, speed=%s',
                      old, self._context.position, getattr(self._context,
                                                        self._parameter),self._context._speed)


class SimulatedMDX5K(StateMachineDevice):
    speed = 1.0

    def _initialize_data(self):
        self.status = 'idle'
        self.interlock = ''
        self.status_command = ''
        self._value = 0.0
        self._voltage = 0.0
        self._current = 0.0
        self._power = 0.0
        self._target = 0.0

    def _get_state_handlers(self):
        return {
            'idle': State(),
            'current': DefaultMovingState('current'),
            'voltage': DefaultMovingState('voltage'),
            'power': DefaultMovingState('power'),

        }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict([
            ])
    #         (('idle', 'moving'), lambda: self.position != self._target),
    #
    #         (('moving', 'idle'), lambda: (self.position == self._target)),
    #
    #     ])

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def current(self):
        return self._current

    @property
    def voltage(self):
        return self._voltage

    @property
    def power(self):
        return self._power

    @voltage.setter
    @check_limits(0, 5000)
    def voltage(self, value):
        self._voltage = value

    @current.setter
    @check_limits(0, 5000)
    def current(self, value):
        self._current = value

    @power.setter
    @check_limits(0, 5000)
    def power(self, value):
        self._power = value

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
        'StatusCommand': PV('status_command', doc='who knows?', type='string'),
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
