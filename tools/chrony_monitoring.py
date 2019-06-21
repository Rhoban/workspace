#! /usr/bin/env python3
import sys
import os
from time import sleep
import datetime
from robot_tools import *
import argparse

def getChronyOffset(host):
    """
    Returns the time offset [s] with the given host
    """
    return float(sshCmd(host, "chronyc -n -c sources").split(",")[-2])

if __name__ == "__main__":
    # Initial comments
    #if len(sys.argv) < 2:
    #    print('Usage: time_client.pt [host1] [host2] ...')
    #    print('host\# should be the name of the robot.')
    #    print('/etc/hosts should contain the conrrespondance between the robot\'s name and its ip.')
    #    exit()
    parser = argparse.ArgumentParser()
    parser.add_argument("hosts", type=str,help="hostnames", nargs="+")
    args = parser.parse_args()

    initial_local_time = float(datetime.datetime.now().timestamp())
    while True:
        sleep(0.5)
        local_time = float(datetime.datetime.now().timestamp()) - initial_local_time
        msg = ""
        msg += str(local_time)
        msg += " "
        for host in args.hosts:
            msg += str(getChronyOffset(host) * 1000)
            msg += " "
        print(msg, end ='\n')
        sys.stdout.flush()
