#!/usr/bin/env python
import threading

from pcaspy import SimpleServer, Driver
import random

prefix_current = 'MHC6:IST:'
pvdb_current = {
    '2': {'prec': 3, 'scan': 0.5, 'type': 'float'},
}

prefix_integrated = 'SQ:AMOR:sumi:'
pvdb_integrated = {
    'SWITCH': { 'type' : 'enum', 'enums': ['Low', 'Hi']},
    'BEAMINT': {'prec': 3, 'scan': 0.1, 'type': 'float'},
}


class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()
        self.eid = threading.Event()
        self.tid = threading.Thread(target = self.runChargeIntegration)
        self.tid.setDaemon(True)
        self.tid.start()

    def read(self, reason):
        if reason == '2':
            value = random.random()
        else:
            value = self.getParam(reason)
        return value

    def write(self, reason, value):
        if reason == 'SWITCH':
            if self.getParam('SWITCH') == 0 and value == 1:
                self.setParam('BEAMINT', 0)
                self.updatePVs()
                self.eid.set()
                self.eid.clear()
        super(myDriver, self).write(reason, value)

    def runChargeIntegration(self):
        updateTime = .1
        while True:
            run = self.getParam('SWITCH')
            if run:
                self.eid.wait(updateTime)
            else:
                self.eid.wait()
            run = self.getParam('SWITCH')
            if not run: continue
            current = self.getParam('2')
            charge = self.getParam('BEAMINT')
            self.setParam('BEAMINT',  charge + current * updateTime)
            self.updatePVs()


if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix_current, pvdb_current)
    server.createPV(prefix_integrated, pvdb_integrated)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
