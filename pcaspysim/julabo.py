#!/usr/bin/env python

import argparse
import signal

from pcaspy import Driver, SimpleServer
from pcaspy.tools import ServerThread
from numpy import random

pvlist = [
"INTP:SP",
"TEMP:SP1",
"INTI:SP",
"INTD:SP",
"EXTP:SP",
"EXTI:SP",
"EXTD:SP",
"HILIMIT:SP",
"LOWLIMIT:SP",
"TEMP:SP2",
"TEMP:SP3",
"STATUSc",
"STATUScc",
"VERSION",
"STATUS",
"DISABLE_POLL",
"DISABLE_EXT",
"MODE:SP",
"EXTSENS:SP",
"SP:SEL:RBV",
"MODE",
"EXTSENS",
"SP:SEL",
"TEMP",
"EXTT",
"TSAFE",
"TEMP:SP1:RBV",
"POWER",
"INTP",
"INTI",
"INTD",
"EXTP",
"EXTI",
"EXTD",
"HILIMIT",
"LOWLIMIT",
"TEMP:SP2:RBV",
"TEMP:SP3:RBV",
]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix', default='ESTIA-JUL25HL-001:',
                    help='Used as prefix for the epics PVs')

    args = ap.parse_args()

    pvdb = {
        pvname: {
            "type": "float",
            "value": 0,
            "description": " |  | Write",
        }
        for pvname in pvlist
    }
    pvdb["MODE"] = {
        'type' : 'enum',
        'enums': ['OFF', 'ON']
    }

    server = SimpleServer()
    server.createPV(args.prefix, pvdb)
    server_thread = ServerThread(server)

    def signal_handler(sig, frame):
        print("Shut down server")
        server_thread.stop()

    signal.signal(signal.SIGINT, signal_handler)
    server_thread.start()
