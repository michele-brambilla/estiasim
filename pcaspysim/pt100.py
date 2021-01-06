#!/usr/bin/env python

import argparse
import signal

from pcaspy import Driver, SimpleServer
from pcaspy.tools import ServerThread

HI_RESOLUTION_PVS = [4, 11]


class Model(Driver):
    def __init__(self):
        super(Model, self).__init__()
        for index in range(1, 14):
            if not index in HI_RESOLUTION_PVS:
                self.setParam(f'AnalogInput_{index:02d}', 100+10*index)
            else:
                self.setParam(f'AnalogInput_{index:02d}', 3333+10*index)

    def read(self, reason):
        value = super(Model, self).read(reason.replace('Calc_out','AnalogInput'))
        if 'Calc_out_' in reason:
            if any(f'{index:02d}' in reason for index in HI_RESOLUTION_PVS):
                return value * 0.05
            return value * 0.1
        return value


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix', default='estia-selpt100-001:',
                    help='Used as prefix for the epics PVs')

    args = ap.parse_args()

    pvdb = {}
    pvdb.update({
        f'AnalogInput_{index:02d}': {
            "type": "float",
            "value": 0,
            "description": " |  | Write",
        } for index in range(1, 14)
    })
    pvdb.update({
        f'Calc_out_{index:02d}': {
            "type": "float",
            "value": 0,
            "description": " |  | Read",
        } for index in range(1, 14)
    })
    pvdb.update({
        f'AnalogStatus_{index:02d}': {
            "type": "float",
            "value": 0,
            "description": " |  | Write",
        } for index in range(1, 14)
    })

    server = SimpleServer()
    server.createPV(args.prefix, pvdb)
    server_thread = ServerThread(server)

    driver = Model()

    def signal_handler(sig, frame):
        print("Shut down server")
        server_thread.stop()

    signal.signal(signal.SIGINT, signal_handler)
    server_thread.start()
