#!/usr/bin/env python
from __future__ import absolute_import

import argparse
from time import sleep

from devices import EpicsDeviceSimulation
from devices.power_supply import MDX5K

from devices.loggersim import log
from devices.sighandler import SignalHandler


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-n', '--names',
                    nargs='+',
                    default=['AE01'],
                    help='Power supply name')

    args = ap.parse_args()

    simulation = EpicsDeviceSimulation(args.prefix, args.names, MDX5K)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
