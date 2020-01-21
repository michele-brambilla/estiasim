#!/usr/bin/env python

import argparse
from time import sleep

from devices.epicsdevicesim import EpicsDevice, EpicsDeviceSimulation
from devices.loggersim import log
from devices.power_supply import MDX5K
from devices.sighandler import SignalHandler

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-n', '--names',
                    nargs='+',
                    default=['AE01'],
                    help='Used as names for the epics PVs')

    args = ap.parse_args()

    log.info(args.names)
    simulation = EpicsDeviceSimulation(args.prefix, args.names, MDX5K)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
