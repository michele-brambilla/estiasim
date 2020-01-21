from __future__ import absolute_import

import threading

import pcaspy.tools

from .approaches import linear
from .utils import run_async

db_base = {
    'Status': {
        'type': 'string',
        'unit': '',
        'description': 'Power supply status  | | Read',
    },
    'Interlock': {
        'type': 'str',
        'unit': '',
        'description': 'Interlock  |  | Read/Write',
    },
    'StatusCommand': {
        'type': 'str',
        'unit': '',
        'description': 'StatusCommand  |  | Read/Write',
    },
    'OutputSetpoint-RBV': {
        'type': 'float',
        'unit': '',
        'description': 'Readback value for the setpoint  |  | Read',
    },
    'Voltage': {
        'type': 'float',
        'unit': 'V',
        'description': 'Target voltage  | V | Write',
    },
    'Current': {
        'type': 'float',
        'unit': 'A',
        'description': 'Target current  | A | Write',
    },
    'Power': {
        'type': 'float',
        'unit': 'W',
        'description': 'Target power  | W | Write',
    },

}


class PowerSupplyDriver(pcaspy.Driver):
    _dt = None

    def __init__(self, pvdb, dt=.1):
        super(PowerSupplyDriver, self).__init__()
        self.pvdb = pvdb
        self.threads = {}
        self._dt = dt

    @run_async
    def _do_ramp(self, parameter, target):
        pv_rbv = 'OutputSetpoint-RBV'
        speed = 10.0
        current = self.getParam(pv_rbv)
        current['unit'] = self.getParam(parameter)['unit']
        while current != target:
            current = linear(current, target, speed, self._dt)
            self.setParam(pv_rbv, current)
            self.updatePV(pv_rbv)

    def write(self, pv, value):
        fields = pv.split(':')
        (name, pv_field) = fields[:2] if len(fields) > 1 else \
            pv.split('-')[:2]

        super(PowerSupplyDriver, self).write(pv, value)
        if pv_field in ['Voltage', 'Current', 'Power']:
            self.threads[pv_field] = threading.Thread(target=self._do_ramp,
                                                        args=(pv_field,
                                                              value)).start()


class PowerSupply(object):

    def __init__(self, name):
        self.name = name
        self.api_device = None
        self.driver = None

    def _get_pv_prefix(self):
        return '%s.' % self.name

    def set_driver(self, driver=PowerSupplyDriver):
        self.driver = driver(self.get_pvdb())

    @staticmethod
    def ret_driver():
        return PowerSupplyDriver

    @staticmethod
    def get_pvdb():
        db = db_base
        return db
