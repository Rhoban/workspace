#!/usr/bin/env python3

from chrony_monitoring import *
from robot_tools import *
import argparse

# key: nb_robots
# value: array with boundaries for each robot [minX maxX, minY maxY]
boundariesNames = ["minX", "maxX", "minY", "maxY"]
defaultBoundaries = { 3: [[-4, -1, -3,  3],
                          [0, 4.0, -0.5,  2.5],
                          [0, 4.0, -2.5, -1.5]],
                      4: [[-4, -0.5, -0.5,  3],
                          [-4, -0.5, -3, -1.5],
                          [0.5, 4.0, -0.5,  3],
                          [0.5, 4.0, -3, -1.5]],
                      5: [[-4.5, -2.5, -1,  1],
                          [-4, -2.5, -3, -0.5],
                          [-4, -2.5, -0.5,  3],
                          [0.5, 4.0, -3, -1.5],
                          [0.5, 4.0, -3, -1.5]]}

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
    rhioCmd('/localisation/field/odometryMode=1', host)

def printBoundaries(host):
    for name in boundariesNames:
        print(name + " -> " + rhioCmd("/moves/vision_log_machine/{:}".format(name)))

def updateBoundaries(host, boundaries):
    if (len(boundaries) != len(boundariesNames)):
        raise RuntimeError("Boundaries len is not valid")
    print("Setting boundaries for " + host)
    for i in range(len(boundaries)):
        name = boundariesNames[i]
        value = boundaries[i]
        print("-> {:} : {:}".format(name, value))
        rhioCmd("/moves/vision_log_machine/{:}={:}".format(name,value), host)

def customBoundaries(host):
    msg("UPDATE_BOUNDARIES", "Defining patrolling area for {:}".format(host))
    boundaries = []
    for i in range(len(boundariesNames)):
        boundaries += [askDouble("Enter value for {:} )".format(boundariesNames[i]))]
    updateBoundaries(host, boundaries)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true",
                        help="initialize robots before launching log vision")
    parser.add_argument("-c", "--customBoundaries", action="store_true",
                        help="Ask the user to specify the custom boundaries")
    parser.add_argument("-d", "--defaultBoundaries", action="store_true",
                        help="Use default boundaries")
    parser.add_argument("hosts", type=str,help="hostname", nargs="+")
    args = parser.parse_args()

    nb_hosts = len(args.hosts)
    if args.defaultBoundaries and not nb_hosts in defaultBoundaries:
        raise RuntimeError("No default boundaries available for {:} hosts".format(nb_hosts))
    msg("SYNC_CHECK", "Checking time offsets with the robots")
    offsets = {}#[ms]
    max_offset = 0;#[ms]
    for host in args.hosts:
        offsets[host] = 1000*getChronyOffset(host)
        max_offset = max(abs(offsets[host]), max_offset)
    print("measured offsets in ms: " + str(offsets))
    if max_offset > 5:
        print("measured offsets are too high, check sync")
        exit(-1)
    if args.init:
        for host in args.hosts:
            defaultInit(host)
    logDuration = askDouble("What is the required duration for log? [s]")
    for host_idx in range(nb_hosts):
        host = args.hosts[host_idx]
        setVariables(host, logDuration)
        if args.customBoundaries:
            customBoundaries(host)
        elif args.defaultBoundaries:
            updateBoundaries(host, defaultBoundaries[nb_hosts][host_idx])
        else:
            printBoundaries(host)
        manualCustomReset(host)

    msg("FINAL", "Press enter to activate vision_log_machine on all robots and start logging")
    sys.stdin.readline()
    for host in args.hosts:
        rhioCmd("vision_log_machine", host)
        rhioCmd("logLocal {:}".format(logDuration), host)

