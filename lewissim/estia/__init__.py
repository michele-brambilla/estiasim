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
    def in_state(self, dt):
        old_position = self._context.position
        self._context._position = approaches.linear(old_position,
                                                    self._context.target,
                                                    self._context.speed, dt)

        self.log.info('Moved position (%s -> %s), target=%s, speed=%s',
                      old_position, self._context.position, self._context.target,
                      self._context.speed)


class SimulatedMotor(StateMachineDevice):
    def _initialize_data(self):
        self._position = 0.0
        self._target = 0.0
        self._speed = 2.0
        self._stop = False
        self.at_home = False
        self.homf = False
        self.homr = True
        self.motor_offset = 0.0
        self.high_limit = 1000.0
        self.low_limit = 0.0
        self.soft_limit = 1.0
        self.high_limit_switch = 1000.0
        self.low_limit_switch = 0.0
        self.cnen = 1
        self.error_message = ''
        self.reset_error = ''
        self.at_home = True
        self.error_bit = 0
        self.set = 0

        self.position_max = 1024
        self.position_min = 0
        self.speed_max = math.pi

    def _get_state_handlers(self):
        return {
            'idle': State(),
            'moving': DefaultMovingState()
        }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('idle', 'moving'), lambda: self.position != self._target),

            (('moving', 'idle'), lambda: (self.position == self._target)),

        ])

    def do_start(self):
        self._stop = False
        if not self.speed > 0.0:
            self.stop = 1

    def do_stop(self):
        """Stops the motor and returns the new target and position, which are equal"""
        self._stop_commanded = True
        self.log.info('Stopping movement after user request.')
        return self.position, self._target

    @property
    def position(self):
        return self._position

    @property
    def target(self):
        return self._target

    @target.setter
    @check_limits('position_min', 'position_max')
    def target(self, value):
        if self.state == 'moving':
            print('Can not set new target while moving.')

        if not (0 <= value <= 250):
            raise ValueError('Target is out of range [%r, %r]' % (
                self.position_min, self.position_max))
        self._target = value
        self.at_home = False

    @property
    def speed(self):
        return self._speed

    @speed.setter
    @check_limits(0.0, 'speed_max')
    def speed(self, value):
        if not (0 <= value <= 250):
            raise ValueError('Target is out of range [0, %r]' % self.speed_max)
        self._speed = value

    @property
    def state(self):
        return self._csm.state

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        if value < 0 or value > 1 or int(value) != value:
            self.log.info('Accepted values are 0, 1.')
        if self.state == 'idle':
            self.log.info('Device in idle state: nothing to do.')
        if value == 1:
            self._stop = True
            self._target = self.position
        self._stop = False

    @property
    def done_moving(self):
        return self.target == self.position

    @property
    def moving(self):
        return self.target != self.position and not self._stop

    @property
    def miss(self):
        return self.target == self.position


class MotorEpicsInterface(EpicsInterface):
    """
    Motor EPICS interface
    """
    pvs = {
        '.RBV': PV('position', read_only=True,
                  doc='Readback value of the position setpoint in mm.'),
        '.VAL': PV('target',
                  doc='Position setpoint in mm.'),
        '.STOP': PV('stop',
                   doc='Force the motor to stop '),
        '.DMOV': PV('done_moving', read_only=True,
                   doc='True if the motor has finished its movement.'),
        '.MOVN': PV('moving', read_only=True,
                   doc='True if the motor is moving.'),
        '.MISS': PV('miss', read_only=True,
                   doc='True if the motor couldn\'t reach the target.'),
        '.HOMF': PV('homf', read_only=True,
                   doc='.'),
        '.HOMR': PV('homr',
                   doc='.'),
        '.VELO': PV('speed', doc='motor_velocity'),
        '.OFF': PV('motor_offset',
                  doc='Initial offset of the motor'),
        '.HLM': PV('high_limit', read_only=True,
                  doc='Hardware high limit in mm'),
        '.LLM': PV('low_limit', read_only=True,
                  doc='Hardware low limit in mm'),
        '.LVIO': PV('soft_limit',
                   doc='Soft limit in mm'),
        '.HLS': PV('high_limit_switch',
                  doc='High limit switch in mm'),
        '.LLS': PV('low_limit_switch',
                  doc='Low limit switch in mm'),
        '.CNEN': PV('cnen'),
        '.SET': PV('set'),
        '-MsgTxt': PV('error_message', read_only=True, type='string',
                     doc='Error message'),
        '.State': PV('state', read_only=True, type='string'),

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


setups = dict(
    moving=dict(
        device_type=SimulatedMotor,
        parameters=dict(
            override_initial_state='moving',
            override_initial_data=dict(
                _target=120.0, _position=20.0
            )
        )
    )
)

framework_version = '1.2.1'
