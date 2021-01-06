from time import sleep

from numpy import random
from pcaspy import Driver

from attocube_statemachine import NarcolepticAttocube

_axis_pvdb = {
    'Displacement_RBV': {
        'type': 'float',
        'value': 0,
        'description': '| | Read',
        'scan': 0.25,
    },
    'AbsolutePosition_RBV': {
        'type': 'float',
        'value': 0,
        'description': '| | Read',
        'scan': 0.25,
    },
    'ConstrastInPermille:Contrast_RBV': {
        'type': 'float',
        'value': 0,
        'description': '| | Read',
        'scan': 0.25,
    },
    'Reset:Error_RBV': {'type': 'int', 'value': 0, 'description': '| | Read',},
    'Reset': {'type': 'int', 'description': ' |  | Write',},
}

current_mode_enum = {
    'system idle': 0,
    'measurement starting': 1,
    'measurement running': 2,
    'optics alignment starting': 3,
    'optics alignment running': 4,
    'pilot laser enabled': 5,
}


pvdb = {
    'PilotLaser:Status_RBV': {
        'type': 'enum',
        'enums': ['off', 'on'],
        'value': 0,
        'description': '| | Read',
        'scan': 0.25,
    },
    'CurrentMode_RBV': {
        'type': 'enum',
        'enums': list(current_mode_enum),
        'value': 0,
        'description': '|  | Read',
        'scan': 0.25,
    },
    'EnableDisablePilotlaser:Error_RBV': {},
    'StartStopMeasurement:Error_RBV': {},
    'StartStopOpticsAlignment:Error_RBV': {},
    'StartStopMeasurement': {
        'type': 'enum',
        'enums': ['off', 'on'],
        'value': 0,
        'description': ' |  | Write',
    },
    'StartStopOpticsAlignment': {
        'type': 'enum',
        'enums': ['off', 'on'],
        'value': 0,
        'description': ' |  | Write',
    },
    'EnableDisablePilotlaser': {
        'type': 'enum',
        'enums': ['off', 'on'],
        'value': 0,
        'description': ' |  | Write',
    },
}


for axis in range(1, 4):
    for key, value in _axis_pvdb.items():
        pvdb.update({f'Axis{axis}:{key}': value})


class Model(Driver):
    def __init__(self):
        self.machine = NarcolepticAttocube('attocube')
        super().__init__()

    def write(self, reason, value):
        print(f'reason: {reason} -> {value}')
        super().write(reason, value)
        if reason == 'EnableDisablePilotlaser':
            if not value:
                self.machine.disable_laser()
                print(self.machine.state)
                return
            self.machine.enable_laser()
            print(self.machine.state)
            return
        if reason == 'StartStopOpticsAlignment':
            # run alignment in a thread
            self.machine.align()
        if reason == 'StartStopMeasurement':
            # run measurement in a thread
            self.machine.measure()

    def read(self, reason):
        if reason == 'CurrentMode_RBV':
            return current_mode_enum[self.machine.state]
        if reason == 'PilotLaser:Status_RBV':
            if self.machine.state == 'pilot laser enabled':
                return 1
            return 0
        if 'ConstrastInPermille:Contrast_RBV' in reason:
            return 10 + abs(random.randn())
        if 'Displacement_RBV' in reason:
            return (1e2 + random.randn()) * 1e3
        if 'AbsolutePosition_RBV' in reason:
            return (1e2 + random.randn()) * 1e3
        return self.getParam(reason)
