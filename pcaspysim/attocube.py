#!/usr/bin/env python

import argparse
import signal

from pcaspy import SimpleServer
from pcaspy.tools import ServerThread

from attocube_model import Model, pvdb


def main(args):

    server = SimpleServer()
    server.createPV(args.prefix, pvdb)

    server_thread = ServerThread(server)
    driver = Model()

    def signal_handler(sig, frame):
        print("Shut down server")
        server_thread.stop()

    signal.signal(signal.SIGINT, signal_handler)
    server_thread.start()



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p",
        "--prefix",
        default="ESTIA-ATTOCUBE-001:",
        help="Used as prefix for the epics PVs",
    )

    args = ap.parse_args()
    main(args)
    # machine = NarcolepticAttocube('attocube')
    # print(machine.state)
    # machine.enable_laser()
    # print(machine.state)
    # machine.align()
    # print(machine.state)
    # machine.disable_laser()
    # print(machine.state)
