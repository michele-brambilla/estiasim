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
        self.position = 0.0
        self._target = 0.0
        self.speed = 2.0

    def _get_state_handlers(self):
        return {
            'idle': State(),
            'moving': DefaultMovingState()
        }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('idle', 'moving'), lambda: self.position != self.target),
            (('moving', 'idle'), lambda: self.position == self.target)])

    @property
    def state(self):
        return self._csm.state

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, new_target):
        if self.state == 'moving':
            raise RuntimeError('Can not set new target while moving.')

        if not (0 <= new_target <= 250):
            raise ValueError('Target is out of range [0, 250]')

        self._target = new_target

    @property
    def target_position(self):
        return self.position

    def stop(self):
        """Stops the motor and returns the new target and position, which are equal"""

        self._target = self.position

        self.log.info('Stopping movement after user request.')

        return self.target, self.position

framework_version = '1.2.0'