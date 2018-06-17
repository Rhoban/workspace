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
    print("== Starting the procedure to get datas. ==")
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
    _,_,returncode= bash_command("ping -c 1 -W 2 10.0.0.1")
    if returncode== 0:
      ip="10.0.0.1"

    _,_,returncode= bash_command("ping -c 1 -W 1 10.3.0.1")
    if returncode== 0:
      ip="10.3.0.1"
    
    print("Changing the vision_config.json.")
    bash_command("cd %s/env/%s && ln -sf ../common/vision_filters/aruco_calib.json vision_config.json"%(workspace_path,robot))
    print("Press enter to deploy-env.")
    raw_input()
    bash_command("xterm -e \"cd %s && ./deploy-env %s\""%(workspace_path,ip))
    
    print("Press enter to run the robot")
    raw_input()
    bash_command("xterm -e \"%s/run %s\""%(workspace_path,ip))


    print("Is the focus of the camera okay ? (Check the white point on the camera.)")
    print("Press enter to continue.")
    raw_input()

    
    print("Prepare robot to be initialised+walk. (Wait for the robot to be ready.)")
    print("Press enter when ready.")
    raw_input()

    bash_command("rhio %s init"%(ip,))
    bash_command("rhio %s walk"%(ip,))

    print("Put the robot in the aruco calibration setup.")
    print("Press enter to continue.")
    raw_input()

    print("If needed tune the threshold/shutter/gain parameters.")
    bash_command("rhio 10.0.0.1 moves/head/disabled=false")
    bash_command("rhio 10.0.0.1 moves/head/maxSpeed=30")
    bash_command("rhio 10.0.0.1 head")
    bash_command("xterm -e \"rhio 10.0.0.1 view Vision/tagsDetector/out\"")
    print("Press enter to continue and stop the head.")
    resp=raw_input().lower()
    bash_command("rhio 10.0.0.1 moves/head/disabled=true")

    print("Press enter when ready to lunch the calibration.")
    raw_input()

    bash_command("rhio %s arucoCalibration"%(ip,))
    print("Press enter when calibration is finished.")
    raw_input()


    cmd="mkdir -p %s"%folder
    bash_command(cmd)

    print("Retrieving the aruco file.")
    cmd="scp rhoban@%s:~/env/%s/arucoCalibration.csv %s"%(ip,robot,aruco)
    _,_,code=bash_command(cmd)
    cmd="cp %s %s/%s"%(aruco,folder,aruco)
    _,_,code=bash_command(cmd)

    if code!=0:
        print("Error on recovering aruco file")
        sys.exit(1)

    resp="not"
    while not resp in ["","n","y"]:
        print("Do you want to lunch the model training ?[n/Y]")
        print("It is usefull to check if there is something wrong.")
        resp=raw_input().lower()

        if resp=="n":
            sys.exit(0)

print("\n")
print("== Starting the training. ==")
cmd="cp model_learning_analyzer \
    vision_correction_analyzer_fast_test.json \
    vision_correction_debug \
    vision_correction_debug.json \
    vision_input_reader.json \
    sigmaban.urdf \
    default_vision_correction_model.json \
    plot_vision_debug.r \
    plot_graph.r \
    %s"%folder
_,err,code=bash_command(cmd)

if code==1: 
    print(err)
    sys.exit(1)

os.chdir(folder)

cmd="./model_learning_analyzer vision_correction_analyzer_fast_test.json %s"%aruco
bash_command(cmd)

out=glob.glob("*average*")

print("Starting the creation of debug graphics.")
print("(Should lunch plot_graph.)")
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

if local_file==False:
    print("Remove the robot from the setup and press enter when ready to em")
    raw_input()

    bash_command("rhio 10.0.0.1 em")

    resp="not"
    while not resp in ["","n","y"]:
        print("Change vision_filter back to all.json with \"git checkout %s/env/%s/vision_config.json\" and deploy-env? [Y/n]"%(workspace_path,robot))
        resp=raw_input().lower()

    if resp=="y":
        bash_command("git checkout %s/env/%s/vision_config.json")
        bash_command("%s/deploy-env %s"%(workspace_path,ip))
    raw_input()
    print("Press enter to halt the robot")
    bash_command("%s/halt %s"(workspace_path,ip))

os.chdir("..")
print("Finished")
sys.exit(0)
