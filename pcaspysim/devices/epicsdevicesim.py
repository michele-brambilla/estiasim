from __future__ import absolute_import

import pcaspy
import pcaspy.tools

from .loggersim import log


class EpicsDevice(object):

    _pvdb = {}

    def __init__(self, prefix, dev_names, dev_type, driver=None):
        self.prefix = '%s:' % prefix if prefix else ''

        self.devices = {}
        for dev_name in dev_names:
            device = dev_type(dev_name)
            self.devices[dev_name] = device
            self._pvdb.update(device.get_pvdb())

        self.server = pcaspy.SimpleServer()
        self.server.createPV(self.prefix, self._pvdb)
        self.server_thread = pcaspy.tools.ServerThread(self.server)

        for device in list(self.devices.values()):
            if driver:
                device.set_driver(driver)
            else:
                device.set_driver()

    def start(self):
        # process CA transactions
        self.server_thread.start()
        return

    def stop(self):
        log.info('{}::stop'.format(type(self).__name__))
        self.server_thread.stop()


class EpicsDeviceSimulation(object):
    def __init__(self, prefix, dev_names, device):
        self.device = EpicsDevice(prefix, dev_names, device, driver=None)

    def start(self):
        self.device.start()

    def stop(self):
        try:
            log.info('stopping simulation')
            self.device.stop()
        except Exception as e:
            log.info('Simulation did not shut down cleanly : %r.' % e)
