#!/usr/bin/env python3

from robot_tools import *
import argparse


def setVariables(host):
    msg('AUTO', "Setting all variables on " + host)
    msg('AUTO', "Stopping head")
    rhioCmd('stop head', host)
    msg('AUTO', "Disabling torque head")
    rhioCmd('/lowlevel/head_pitch/torqueEnable=false', host)
    rhioCmd('/lowlevel/head_yaw/torqueEnable=false', host)
    msg('AUTO', "Disabling calibration")
    rhioCmd('/model/useCalibration=false', host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hosts", type=str,help="hostname", nargs="+")
    args = parser.parse_args()
    host = args.hosts[0]

    logDuration = askDouble("What is the required duration for log? [s]")
    setVariables(host)
    msg("FINAL", "Press enter to activate horizon log.")
    sys.stdin.readline()
    rhioCmd("logLocal {:}".format(logDuration), host)

