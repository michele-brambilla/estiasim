from __future__ import absolute_import

import pcaspy
import pcaspy.tools

from pcaspysim.devices.loggersim import log
from pcaspysim.devices.motorsim import Motor, MotorEpicsDriver


class EpicsDevice(object):

    _pvdb = {}

    def __init__(self, name, mot_names):
        self.name = name

        self.motors = {}
        for motor_name in mot_names:
            motor = Motor(motor_name)
            self.motors[motor_name] = motor
            self._pvdb.update(motor.get_pvdb())

        self.server = pcaspy.SimpleServer()
        self.server.createPV(self.name + ':', self._pvdb)
        self.server_thread = pcaspy.tools.ServerThread(self.server)

        self.driver = MotorEpicsDriver(self, self._pvdb)

        for _, motor in self.motors.items():
            motor.set_driver(self.driver)

    def start(self):
        # process CA transactions
        self.server_thread.start()
        return

    def stop(self):
        log.info('{}::stop'.format(type(self).__name__))
        self.server_thread.stop()


class EpicsDeviceSimulation(object):
    def __init__(self, name, mot_names, device=EpicsDevice):
        self.device = device(name, mot_names)

    def start(self):
        self.device.start()

    def stop(self):
        try:
            log.info('stopping simulation')
            self.device.stop()
        except Exception as e:
            log.info('Simulation did not shut down cleanly : %r.'%e)
