#!/usr/bin/env python

import argparse
from time import sleep

from devices.epicsdevicesim import EpicsDevice, EpicsDeviceSimulation
from devices.loggersim import log
from devices.sighandler import SignalHandler


class MetronomyCart(EpicsDevice):
    pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--cart-name',
                    default='PSI-ESTIARND:MC-MCU-01',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-m', '--motor-names',
                    nargs='+',
                    default=['m1', 'm2'],
                    help='Used as names for the epics PVs')

    args = ap.parse_args()

    log.info(args.motor_names)
    simulation = EpicsDeviceSimulation(args.cart_name, args.motor_names,
                                       MetronomyCart)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
