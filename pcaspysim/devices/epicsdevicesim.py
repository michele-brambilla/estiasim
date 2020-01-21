from __future__ import absolute_import

import pcaspy
import pcaspy.tools

from .loggersim import log
from .motorsim import Motor, MotorEpicsDriver


class EpicsDevice(object):

    _pvdb = {}

    def __init__(self, prefix, dev_names, dev_type):
        self.prefix = prefix

        self.devices = {}
        for dev_name in dev_names:
            device = dev_type(dev_name)
            self.devices[dev_name] = device
            self._pvdb.update(device.get_pvdb())

        self.server = pcaspy.SimpleServer()
        self.server.createPV('%s:'self.prefix if self.prefix else '', self._pvdb)
        self.server_thread = pcaspy.tools.ServerThread(self.server)

        self.driver = dev_type._default_driver(self, self._pvdb)

        for device in list(self.devices.values()):
            device.set_driver(self.driver)

    def start(self):
        # process CA transactions
        self.server_thread.start()
        return

    def stop(self):
        log.info('{}::stop'.format(type(self).__name__))
        self.server_thread.stop()


class EpicsDeviceSimulation(object):
    def __init__(self, prefix, dev_names, device):
        self.device = EpicsDevice(prefix, dev_names, device)

    def start(self):
        self.device.start()

    def stop(self):
        try:
            log.info('stopping simulation')
            self.device.stop()
        except Exception as e:
            log.info('Simulation did not shut down cleanly : %r.'%e)
