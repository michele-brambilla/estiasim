#!/usr/bin/env python
from __future__ import absolute_import

import argparse
from time import sleep

from devices import EpicsDevice, EpicsDeviceSimulation, SignalHandler, log


class SeleneGuide(EpicsDevice):
    pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--guide-name',
                    default='PSI-ESTIARND:MC-MCU-01',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-m', '--motors-name',
                    nargs='+',
                    default=['m10', 'm11', 'm12', 'm13', 'm14'],
                    help='Used as names for the epics PVs')

    args = ap.parse_args()

    simulation = EpicsDeviceSimulation(args.guide_name, args.motors_name,
                                       SeleneGuide)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
