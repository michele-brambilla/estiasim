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

"""
Defines functions that model typical behavior, such as a value approaching a target linearly at
a certain rate.
"""

from time import sleep


def linear(current, target, rate, dt):
    sign = (target > current) - (target < current)

    if not sign:
        return current
    new_value = current + sign * rate * 1e-3*dt

    if sign * new_value > sign * target:
        return target

    sleep(1e-3*dt)
    return new_value
