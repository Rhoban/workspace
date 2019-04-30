#! /usr/bin/env python
# coding: utf-8

from subprocess import Popen, PIPE
import sys
import time

workspace_path="~/private/recherche/robhan/workspace"

def bash_command(cmd):
    proc = Popen(['/bin/bash'], stdin=PIPE)
    return proc.communicate(cmd)+(proc.returncode,)


argv=sys.argv
if len(argv) != 3 or argv[2] not in {"front", "back"}:
    print("Usage : %s <robot_name> <front/back>"%argv[0])
    sys.exit(1)

robot = argv[1]
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

print("Press enter to lunch init.")
raw_input()
bash_command("rhio %s init"%(ip,))

print("Press enter to run gyroTare.")
print("The robot should be standing still.")
raw_input()
bash_command("rhio %s gyroTare"%(ip,))
while True:
    print("Did it work ? [n/Y]")
    resp=raw_input().lower()
    if not resp=="n":
        break

if argv[2]=="back":
    bash_command("rhio %s /moves/standup_imu_calibration/front=false"%(ip,))

bash_command("rhio %s stop standup_imu_calibration"%(ip,))
bash_command("rhio %s standup_imu_calibration"%(ip,))

while True:
    print("Do you want to lunch a standup ? [n/Y]")
    resp=raw_input().lower()
    if resp in {"n"}:
        bash_command("rhio %s stop standup_imu_calibration"%(ip,))
        break
    else:
        print("Press enter when the robot "+ side +" in on the ground again.")
        raw_input()
        bash_command("rhio %s /moves/standup_imu_calibration/lunch=true"%(ip,))

# waits for standup_imu_calibration to generate the csv files
time.sleep(1)
bash_command("mkdir tmp_imu_during_standup")
if robot!="fake":
    bash_command("scp rhoban@%s:~/env/%s/imu_trajectories.csv tmp_imu_during_standup"%(ip,robot))
    bash_command("ssh rhoban@%s \"rm ~/env/%s/imu_trajectories.csv\""%(ip,robot))

    bash_command("scp rhoban@%s:~/env/%s/imu_model.csv tmp_imu_during_standup"%(ip,robot))
    bash_command("ssh rhoban@%s \"rm ~/env/%s/imu_model.csv\""%(ip,robot))
else:
    bash_command("cp ../env/fake/imu_trajectories.csv tmp_imu_during_standup")
    bash_command("rm ../env/fake/imu_trajectories.csv")

    bash_command("cp ../env/fake/imu_model.csv tmp_imu_during_standup")
    bash_command("rm ../env/fake/imu_model.csv")

print("Do you want to delete the tmp folder ? [n/Y]")
resp=raw_input().lower()
if not resp == "n":
    bash_command("mkdir tmp_imu_during_standup")
