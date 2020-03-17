#!/usr/bin/env python

import argparse

from pcaspy import Driver, SimpleServer


class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='PSI-ESTIARND:MC-MCU-01:',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-n', '--names',
                    nargs='+',
                    default=['Limit_Coll', 'Limit_Free'],
                    help='Used as names for the epics PVs')

    args = ap.parse_args()

    pvdb = {}
    for pv in args.names:
        pvdb.update({ pv : {'prec' : 3} })

    server = SimpleServer()
    server.createPV(args.prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
