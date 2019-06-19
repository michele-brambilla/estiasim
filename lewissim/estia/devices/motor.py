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

from collections import OrderedDict

from lewis.core import approaches
from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice


class DefaultMovingState(State):
    def in_state(self, dt):
        old_position = self._context.position
        self._context.position = approaches.linear(old_position,
                                                   self._context.target,
                                                   self._context.speed, dt)
        self.log.info('Moved position (%s -> %s), target=%s, speed=%s',
                      old_position,
                      self._context.position, self._context.target,
                      self._context.speed)


class SimulatedMotor(StateMachineDevice):
    def _initialize_data(self):
        self._position = 0.0
        self._target = 0.0
        self.speed = 2.0
        self._stop = False
        self.at_home = False
        self.homf = False
        self.homr = True
        self.motor_offset = 0.0
        self.high_limit=1000.0
        self.low_limit = 0.0
        self.soft_limit = 1.0
        self.high_limit_switch = 1000.0
        self.low_limit_switch = 0.0
        self.cnen=1
        self.error_message=''
        self.reset_error=''
        self.at_home=True
        self.error_bit=0

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
    def state(self):
        return self._csm.state

    @property
    def position(self):
        return self._position

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, new_target):
        if self.state == 'moving':
            print('Can not set new target while moving.')

        if not (0 <= new_target <= 250):
            raise ValueError('Target is out of range [0, 250]')
        self._target = new_target
        self.at_home = False

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


framework_version = '1.2.0'
