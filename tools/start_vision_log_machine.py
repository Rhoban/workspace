#!/usr/bin/env python3

from robot_tools import *
import argparse

def setVariables(host, logDuration):
    msg('AUTO', "Setting all variables on " + host)
    msg('AUTO', "Setting duration of runs to {:} seconds".format(logDuration))
    rhioCmd("/moves/vision_log_machine/runDuration={:}".format(logDuration), host)
    msg('AUTO', "Customizing head parameters")
    rhioCmd('/moves/head/maxSpeed=60', host)
    rhioCmd('/moves/head/maxAcc=600', host)
    rhioCmd('/moves/head/minOverlap=20', host)
    rhioCmd('/moves/head/maxPan=160', host)
    msg('AUTO', "Reducing walk limits")
    rhioCmd('/moves/walk/maxRotation=10', host)
    rhioCmd('/moves/walk/maxStep=0.06', host)
    rhioCmd('/moves/walk/maxLateral=0.03', host)
    # It might not be necessary, old problem was to have too much similar data to label manually
    # Now, 40 fps should not require more human work
    #msg('AUTO', "Reducing framerate to 25 FPS")
    #rhioCmd('/Vision/source/FrameRate/absValue=25', host)
    msg('AUTO', "Reducing handledDelay")
    rhioCmd('decision/handledDelay=0.01', host)
    msg('AUTO', "Enabling odometryMode")
    rhioCmd('/localisation/field/odometryMode=0', host)

def updateBoundaries(host):
    msg("UPDATE_BOUNDARIES", "Defining patrolling area for {:}".format(host))
    boundaries = {"minX" : -4.5, "maxX" : 4.5, "minY" : -3, "maxY" : 3}
    for k,v in boundaries.items():
        newVal = askDouble("Enter value for {:} (default: {:})".format(k,v))
        rhioCmd("/moves/vision_log_machine/{:}={:}".format(k,newVal), host)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true",
                        help="initialize robots before launching log vision")
    parser.add_argument("hosts", type=str,help="hostname", nargs="+")
    args = parser.parse_args()

    logDuration = askDouble("What is the required duration for log? [s]")
    
    if args.init:
        for host in args.hosts:
            defaultInit(host)
    for host in args.hosts:
        setVariables(host, logDuration)
        updateBoundaries(host)
        manualCustomReset(host)
    # TODO: define global areas
    msg("FINAL", "Press enter to activate vision_log_machine on all robots and start logging")
    sys.stdin.readline()
    for host in args.hosts:
        rhioCmd("vision_log_machine", host)
        rhioCmd("logLocal {:}".format(logDuration), host)

