#! /usr/bin/env python
# coding: utf-8

from subprocess import Popen, PIPE
import os
import sys
import datetime
import re
import glob
import time 

def bash_command(cmd):
    proc = Popen(['/bin/bash'], stdin=PIPE)
    return proc.communicate(cmd)+(proc.returncode,)


argv=sys.argv
if len(argv)<2:
    print("Usage : %s <robot_name> [optional : path to arucoFile]"%argv[0])
    sys.exit(1)
else:
    robot=argv[1]
    local_file=False
    if len(argv)==3:
        local_file=True

date_obj = datetime.datetime.now()
year=date_obj.year
month=date_obj.month
day=date_obj.day
hour=date_obj.hour
minute=date_obj.minute
sec=date_obj.second

date="%04d-%02d-%02d_%02dh%02ds%02d"%(year,month,day,hour,minute,sec)
folder="%s/%s_model_learning_%s"%(robot,robot,date)
aruco="%s_arucoCalibration_%s.csv"%(robot,date)

if local_file:
    cmd="mkdir -p %s"%folder
    bash_command(cmd)
    cmd="cp %s %s/%s"%(argv[2],folder,aruco)
    bash_command(cmd)
else:
    print("\n")
    print("== Retrieving the aruco file. ==")
    if robot=="olive":
        ip="10.1.0.101"
    elif robot=="mowgly":
        ip="10.1.0.102"
    elif robot=="arya":
        ip="10.1.0.103"
    elif robot=="tom":
        ip="10.1.0.104"
    elif robot=="chewbacca":
        ip="10.1.0.105"
    elif robot=="django":
        ip="10.1.0.106"


    # Check if the computer is connected with usb/ethernet.
    # If it is the case, use this connection.
    print("Checking if connected to robot with ethernet")
    _,_,returncode= bash_command("ping -c 1 -W 1 10.0.0.1")
    if returncode== 0:
      ip="10.0.0.1"

    _,_,returncode= bash_command("ping -c 1 -W 1 10.3.0.1")
    if returncode== 0:
      ip="10.3.0.1"

    make_calib="not"
    while not make_calib in ["","n","y"]:
        print("Do you want to lunch calibration on the robot ?[N/y]")
        make_calib=raw_input().lower()

    if make_calib=="y":
        print("Is the focus of the camera okay ? (Check the white point on the camera.)")
        print("Press enter to continue.")
        raw_input()

        print("Did you change the vision_config file and deployed ?")
        print("Press enter to continue.")
        raw_input()

        print("Prepare robot to be initialised+walk. (The server needs to be on.)")
        print("Press enter when ready.")
        raw_input()

        bash_command("rhio %s init"%(ip,))
        bash_command("rhio %s walk"%(ip,))

        print("Put the robot in the aruco calibration setup.")
        print("Press enter to continue.")
        raw_input()

        print("Did you tune the threshold/shutter/gain parameters ? (y/N)")
        resp=raw_input().lower()

        if resp=="n":
            bash_command("rhio %s /moves/head/disabled=false")
            bash_command("rhio %s head")

        print("Press enter when ready to lunch the calibration.")
        raw_input()

        bash_command("rhio %s arucoCalibration"%(ip,))
        print("Press enter when calibration is finished.")
        raw_input()


    cmd="mkdir -p %s"%folder
    bash_command(cmd)

    print("Retrieving the aruco file.")
    cmd="scp rhoban@%s:~/env/%s/arucoCalibration.csv %s/%s"%(ip,robot,folder,aruco)
    _,_,code=bash_command(cmd)

    if code!=0:
        print("Error on recovering aruco file")
        sys.exit(1)

    resp="not"
    while not resp in ["","n","y"]:
        print("Do you want to lunch the model training ?[n/Y]")
        resp=raw_input().lower()

        if resp=="n":
            sys.exit(0)

print("\n")
print("== Starting the training. ==")
cmd="cp model_learning_analyzer \
    vision_correction_analyzer.json \
    vision_correction_debug \
    vision_correction_debug.json \
    vision_input_reader.json \
    sigmaban.urdf \
    default_vision_correction_model.json \
    plot_vision_debug.r \
    %s"%folder
_,err,code=bash_command(cmd)

if code==1: 
    print(err)
    sys.exit(1)

os.chdir(folder)

cmd="./model_learning_analyzer vision_correction_analyzer.json %s"%aruco
bash_command(cmd)

out=glob.glob("*average*")

print("Starting the creation of debug graphics.")
# Change vision_correction_debug file
for model in out:
    # Change the path to the model which will be compared with the default model
    fr=open("vision_correction_debug.json","r")
    fw=open("vision_correction_debug_tmp.json","w")
    for line in fr:
        if "trained" in line:
            i=re.search("[^\"]*\"}",line).start() #
            new_line=line[:i]+model+"\"}"
            fw.write(new_line)
        else:
            fw.write(line)
    fr.close()
    fw.close() 
#Launch
    cmd="./vision_correction_debug vision_correction_debug_tmp.json vision_input_reader.json %s"%aruco
    bash_command(cmd)

    cmd="Rscript plot_vision_debug.r debug.csv"
    bash_command(cmd)

    cmd="mv vision_debug.png vision_debug_"+model[:-5]+".png"
    bash_command(cmd)

out=glob.glob("_parameters.csv")
for model in out:
    cmd="Rscript plot_graph.r -m parameters %s.csv"%model
    bash_command(cmd)

    cmd="mv parameters_analysis parameters_analysis"+model[:-15]+".png"
    bash_command(cmd)

if make_calib=="y":
    print("Change vision_filter back to all.json")
    print("Deploy env.")
    raw_input()

os.chdir("..")
print("Finished")
sys.exit(0)
