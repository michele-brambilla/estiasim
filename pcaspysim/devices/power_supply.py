from __future__ import absolute_import

import threading

import pcaspy.tools
from pcaspy import Severity

from .approaches import linear
from .loggersim import log
from .utils import run_async

db_base = {
    'RBV': {
        'type': 'float',
        'unit': 'mm',
        'description': 'PV readback value  | mm | Read',
    },
    'VAL': {
        'type': 'float',
        'unit': 'mm',
        'description': 'PV value  | mm | Write',
        'asyn': True
    },
    'STOP': {
        'type': 'int',
        'value': 0,
        'states': [Severity.NO_ALARM, Severity.MINOR_ALARM]
    },
    'DMOV': {
        'type': 'int',
        'value': 1,
        'states': [Severity.NO_ALARM, Severity.MINOR_ALARM]
    },
    'MOVN': {
        'type': 'int',
        'value': 0,
        'states': [Severity.NO_ALARM, Severity.MINOR_ALARM]
    },
    'MISS': {
        'type': 'int',
        'value': 0,
        'states': [Severity.NO_ALARM, Severity.MINOR_ALARM]
    },
    'HOMF': {
        'type': 'int',
        'lolim': 0,
        'hilim': 1,
    },
    'HOMR': {
        'type': 'int',
        'lolim': 0,
        'hilim': 1,
    },
    'VELO': {
        'type': 'float',
        'unit': 'mm/s',
        'description': 'Motor speed | mm/s | Read',
    },
    'OFF': {
        'type': 'float',
        'unit': 'mm',
        'description': 'Offset | mm | Read/Write',
    },
    'HLM': {
        'type': 'float',
        'unit': 'mm',
        'description': 'High limit | mm | Read',
    },
    'LLM': {
        'type': 'float',
        'unit': 'mm',
        'description': 'Low limit | mm | Read',
    },
    'LVIO': {
        'type': 'float',
        'unit': 'mm',
        'description': 'Soft limit | mm | Read/Write',
    },
    'HLS': {
        'type': 'float',
        'unit': 'mm',
        'description': 'High limit switch | mm | Read/Write',
    },
    'LLS': {
        'type': 'float',
        'unit': 'mm',
        'description': 'Low limit switch | mm | Read/Write',
    },
    'CNEN': {
        'type': 'int',
        'description': 'Enable',
    },
    'MsgTxt': {
        'type': 'string',
        'description': 'Error message'
    },
    'ErrRst': {
        'type': 'string',
        'description': 'Error message'
    },
    'Err': {
        'type': 'string',
        'description': 'Error message'
    },

}


class MotorEpicsDriver(pcaspy.Driver):
    _dt = None

    def __init__(self, pvdb, dt=10):
        super(MotorEpicsDriver, self).__init__()
        self.pvdb = pvdb
        self.threads = {}
        self._dt = dt

        for pv in pvdb:
            self.setParamStatus(pv, 0, 0)
            if 'VELO' in pv:
                self.setParam(pv, 10.0)
            if 'HLM' in pv:
                self.setParam(pv, 100000.0)
            if 'LLM' in pv:
                self.setParam(pv, -10000.0)
            if 'DMOV' in pv:
                self.setParam(pv, 1)
            if 'CNEN' in pv:
                self.setParam(pv, 1)

    @run_async
    def _do_move(self, motor_name, target):

        # TODO: implement stop
        pv_rbv = motor_name + '.RBV'
        pv_moving = motor_name + '.MOVN'
        pv_done_moving = motor_name + '.DMOV'
        motor_speed = self.getParam(motor_name + '.VELO')

        if self.getParam(pv_moving):
            log.warn('Motor is moving, unable to change target')
            return

        self.setParam(pv_moving, 1)
        self.setParam(pv_done_moving, 0)

        [self.updatePV(pv) for pv in (pv_moving, pv_done_moving)]

        if not motor_speed:
            log.warning('motor speed is null, unable to move')
            return self.getParam(pv_rbv)

        current = self.getParam(pv_rbv)
        while current != target:
            current = linear(current, target, motor_speed,
                                        self._dt)
            self.setParam(pv_rbv, current)
            self.updatePV(pv_rbv)

        if current is not target:
            self.setParam(pv_rbv, float(target))

        self.setParam(pv_moving, 0)
        self.setParam(pv_done_moving, 1)
        [self.updatePV(pv) for pv in (pv_moving, pv_done_moving, pv_rbv)]

    def write(self, pv, value):
        fields = pv.split('.')
        (motor_name, pv_field) = fields[:2] if len(fields) > 1 else \
            pv.split('-')[:2]

        super(MotorEpicsDriver, self).write(pv, value)
        if pv_field == 'VAL':
            self.threads[motor_name] = threading.Thread(target=self._do_move,
                                                        args=(motor_name,
                                                              value)).start()


class Motor(object):

    def __init__(self, name):
        self.name = name
        self.api_device = None
        self.driver = None

    def _get_pv_prefix(self):
        return '%s.' % self.name

    def set_driver(self, driver=MotorEpicsDriver):
        self.driver = driver(self.get_pvdb())

    def ret_driver(self):
        return MotorEpicsDriver

    def get_pvdb(self):
        db = {}
        for field in db_base:
            if field not in ['MsgTxt', 'ErrRst', 'Err']:
                db[self._get_pv_prefix() + field] = db_base[field]
            else:
                db[self.name + '-' + field] = db_base[field]
        return db
