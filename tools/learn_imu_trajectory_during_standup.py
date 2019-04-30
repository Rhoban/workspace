#! /usr/bin/env python
# coding: utf-8

from subprocess import Popen, PIPE
import os
import sys
import datetime
import re
import glob
import time 

workspace_path="~/private/recherche/robhan/workspace"

def bash_command(cmd):
    proc = Popen(['/bin/bash'], stdin=PIPE)
    return proc.communicate(cmd)+(proc.returncode,)


argv=sys.argv
if len(argv) != 3 or argv[2] not in {"front", "back"}:
    print("Usage : %s <robot_name> <front/back>"%argv[0])
    sys.exit(1)

side = argv[2]

if robot=="olive":
    ip="10.1.0.101"
elif robot=="nova":
    ip="10.1.0.102"
elif robot=="arya":
    ip="10.1.0.103"
elif robot=="tom":
    ip="10.1.0.104"
elif robot=="rush":
    ip="10.1.0.105"
elif robot=="fake":
    ip="127.0.0.1"
else:
    print("Robot name is not valid. It should be one of the following:")
    print("olive, nova, arya, tom, rush or fake.")
    sys.exit(1)

# Check if the computer is connected with usb/ethernet.
# If it is the case, use this connection.
print("Checking if connected to robot with ethernet")
_,_,returncode= bash_command("ping -c 1 -W 2 10.0.0.1")
if returncode== 0:
    ip="10.0.0.1"

print("Press enter to lunch init")
raw_input()
bash_command("rhio %s init"%(ip,))
if argv[2]=="back":
    bash_command("rhio /moves/standup_imu_calibration/front=false"%(ip,))

bash_command("rhio %s standup_imu_calibration"%(ip,))

while True:
    print("Do you want to lunch a standup ? [n/Y]")
    resp=raw_input().lower()
    if resp in {"n", "N"}:
        break
    else:
        print("Press enter when the robot "+ side +" in on the ground again.")
        raw_input()
        bash_command("rhio /moves/standup_imu_calibration/lunch=true"%(ip,))

bash_command("mkdir tmp_imu_during_standup")
if robot!="fake":
    bash_command("scp rhoban@%s:~/env/%s/imu_trajectories.csv tmp_imu_during_standup"%(ip,robot))
    bash_command("scp rhoban@%s:~/env/%s/imu_model.csv tmp_imu_during_standup"%(ip,robot))
