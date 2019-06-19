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

from lewis.adapters.epics import PV, EpicsInterface


def MotorEpicsInterfaceFactory(motor_names):
    template = {
        'RBV': PV('target_position', read_only=True,
                  doc='Readback value of the position setpoint in mm.'),
        'VAL': PV('target_position',
                  doc='Position setpoint in mm.'),
        'STOP': PV('stop_state',
                   doc='Force the motor to stop '),
        'DMOV': PV('done_moving', read_only=True,
                   doc='True if the motor has finished its movement.'),
        'MOVN': PV('moving', read_only=True,
                   doc='True if the motor is moving.'),
        'MISS': PV('target_miss', read_only=True,
                   doc='True if the motor couldn\'t reach the target.'),
        'HOMF': PV('homf', read_only=True,
                   doc='.'),
        'HOMR': PV('homr',
                   doc='.'),
        'VELO': PV('speed', read_only=True,
                   doc='motor_velocity'),
        #                       type='enum', enums=['false', 'true']),
        'OFF': PV('motor_offset',
                  doc='Initial offset of the motor'),
        'HLM': PV('high_limit', read_only=True,
                  doc='Hardware high limit in mm'),
        'LLM': PV('low_limit', read_only=True,
                  doc='Hardware low limit in mm'),
        'LVIO': PV('soft_limit',
                   doc='Soft limit in mm'),
        'HLS': PV('high_limit_switch',
                  doc='High limit switch in mm'),
        'LLS': PV('low_limit_switch',
                  doc='Low limit switch in mm'),
        'CNEN': PV('cnen'),
        'MsgTxt': PV('error_message', read_only=True, type='string',
                     doc='Error message'),
        'State': PV('state', read_only=True, type='string'),
    }
    pvs = {}
    for motor in motor_names:
        for key, value in template.items():
            print('%s.%s: %r'%(motor,key, value))


class MotorEpicsInterface(EpicsInterface):
    """
    Motor EPICS interface
    """
    pvs = {
        'RBV': PV('target_position', read_only=True,
                  doc='Readback value of the position setpoint in mm.'),
        'VAL': PV('target_position',
                  doc='Position setpoint in mm.'),
        'STOP': PV('stop_state',
                   doc='Force the motor to stop '),
        'DMOV': PV('done_moving', read_only=True,
                   doc='True if the motor has finished its movement.'),
        'MOVN': PV('moving', read_only=True,
                   doc='True if the motor is moving.'),
        'MISS': PV('target_miss', read_only=True,
                   doc='True if the motor couldn\'t reach the target.'),
        'HOMF': PV('homf', read_only=True,
                   doc='.'),
        'HOMR': PV('homr',
                   doc='.'),
        'VELO': PV('speed', read_only=True,
                   doc='motor_velocity'),
        #                       type='enum', enums=['false', 'true']),
        'OFF': PV('motor_offset',
                  doc='Initial offset of the motor'),
        'HLM': PV('high_limit', read_only=True,
                  doc='Hardware high limit in mm'),
        'LLM': PV('low_limit', read_only=True,
                  doc='Hardware low limit in mm'),
        'LVIO': PV('soft_limit',
                   doc='Soft limit in mm'),
        'HLS': PV('high_limit_switch',
                  doc='High limit switch in mm'),
        'LLS': PV('low_limit_switch',
                  doc='Low limit switch in mm'),
        'CNEN': PV('cnen'),
        'MsgTxt': PV('error_message', read_only=True, type='string',
                     doc='Error message'),
        'State': PV('state', read_only=True, type='string'),

    }

    _commands = {'start': 'start',
                 'stop': 'stop',
                 }

    _last_command = ''

    def __init__(self):
        EpicsInterface.__init__(self)
        MotorEpicsInterfaceFactory(['t1', 't2'])

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
