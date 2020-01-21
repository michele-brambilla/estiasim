#!/usr/bin/env python
from __future__ import absolute_import

import argparse
from time import sleep

from devices.epicsdevicesim import EpicsDeviceSimulation
from devices.loggersim import log
from devices.motorsim import Motor
from devices.sighandler import SignalHandler

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--guide-name',
                    default='PSI-ESTIARND:MC-MCU-01',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-m', '--motor-names',
                    nargs='+',
                    default=['m10', 'm11', 'm12', 'm13', 'm14'],
                    help='Used as names for the epics PVs')

    args = ap.parse_args()

    log.info(args.motor_names)
    simulation = EpicsDeviceSimulation(args.guide_name, args.motor_names,
                                       Motor)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
