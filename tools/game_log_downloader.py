#!/usr/bin/python3
import argparse
import subprocess

from robot_tools import *

def downloadGameLogs(host, game_log_path, dst):
    """
    Download the log at given robot_log_path from host to the target folder.
    The perception logs and lowlevel logs are separated in two different folders.
    """
    # Getting name + preparing folder names
    robot_name = getRobotName(host)
    team_id = "team9"
    robot_path = dst + "/" + team_id + "/" + robot_name
    output_log_path = robot_path + "/output_log"
    print("Checking existence of folder '" + game_log_path + "' on robot " + host)
    checkFolder(host, game_log_path)
    output_logs = game_log_path + "/*.log"
    systemOrRaise(["mkdir", "-p", output_log_path])
    print("Copying output logs from '" + output_logs + "'")
    scpCmd(host, output_logs, output_log_path)
    perception_path = robot_path + "/perception"
    systemOrRaise(["mkdir", "-p", perception_path])
    video_logs = game_log_path + "/*/"
    print("Copying video logs from '" + video_logs + "'")
    scpCmd(host, video_logs, perception_path)

def downloadManualLogs(host, log_path, dst):
    # Getting name + preparing folder names
    robot_name = getRobotName(host)
    team_id = "team9"
    robot_path = dst + "/" + team_id + "/" + robot_name
    print("Checking existence of folder '" + log_path + "' on robot")
    checkFolder(host, log_path)
    perception_path = robot_path + "/perception"
    systemOrRaise(["mkdir", "-p", perception_path])
    video_logs = log_path + "/*/"
    print("Copying video logs from '" + video_logs + "'")
    scpCmd(host, video_logs, perception_path)

def clearLog(host):
    print("Removing log from env/game_logs")
    output_log = sshCmd(host, "find env/"+getRobotName(host)+"/game_logs/ -name \"*.log\" ")
    for log in output_log.split() :
        if question("CLEAR_LOG", "Do you want to remove log " + log +" ?"):
             sshCmd(host, "rm "+ log)

    print("Removing log from env/manual_logs")
    output_log = sshCmd(host, "ls env/"+getRobotName(host)+"/manual_logs/ ")
    for log in output_log.split() :
        if question("CLEAR_LOG", "Do you want to remove log " + log +" ?"):
             sshCmd(host, "rm -rf env/"+getRobotName(host)+"manual_logs/"+ log + "/")  



    print("Removing log from backup_env/")
    output_log = sshCmd(host, "ls backup_env/ ")
    for log in output_log.split() :
        if question("CLEAR_LOG", "Do you want to remove log " + log +" ?"):
             sshCmd(host, "rm -rf backup_env/"+ log + "/")  

             

def clearAllLog(host):
    if question("CLEAR_LOG", "Do you want to remove log from env/ ?"):
        sshCmd(host, "rm -rf env/game_logs/")
        sshCmd(host, "rm -rf env/manual_logs/")
    if question("CLEAR_LOG", "Do you want to remove log from backup_env/ ?"):
        sshCmd(host, "rm -rf backup_env/")  
    

    
def listGameLogs(host):
    return sshCmd(host, "find . -name \"game_logs\" | xargs du -hs | sort -h")

def listManualLogs(host):
    return sshCmd(host, "find . -name \"manual_logs\" | xargs du -hs | sort -h")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd = parser.add_mutually_exclusive_group()
    cmd.add_argument("-l", "--list", action="store_true",
                     help="List the game logs available on the robot")
    cmd.add_argument("-c", "--check", type=str, metavar="PATH",
                     help="Check if a log exist")
    cmd.add_argument("-d", "--download", type=str, nargs=2, metavar="PATH",
                     help="Download a log from LOG_PATH to the folder DST_PATH")
    cmd.add_argument("--download-last",  type=str, metavar="PATH",
                     help="Download log from env in differents robots, PATH is dst")
    parser.add_argument("-m", "--manual", action="store_true",
                        help="Focus on manual logs")
    parser.add_argument("-r", "--remove-log", action="store_true",
                        help="Remove logs  from LOG_PATH")
    parser.add_argument("--all-log", action="store_true",
                        help="Remove ALL logs  from LOG_PATH")
    parser.add_argument("robot", type=str,help="robots hostnames", nargs="+")
    args = parser.parse_args()
    robot = args.robot[0]
    nb_robots = len(args.robot)
    if args.download_last :
        for rb in args.robot :
            if args.manual:
                source = "env/" + getRobotName(rb) + "/manual_logs"
                downloadManualLogs(rb, source, args.download_last)
            else:
                source = "env/" + getRobotName(rb) + "/game_logs"
                downloadGameLogs(rb, source, args.download_last)
    elif args.remove_log:
            for rb in args.robot :
                print("removing log on " +getRobotName(rb))
                if args.all_log :
                    clearAllLog(rb)
                else :
                    clearLog(rb)
    else:
        if nb_robots != 1 :
            print ("only option --download_last is avaible for multiple robot")
        elif args.list:
            if args.manual:
                print(listManualLogs(robot))
            else:
                print(listGameLogs(robot))
        elif args.check:
            checkFolder(robot,args.check)
        elif args.download:
            if args.manual:
                downloadManualLogs(robot, args.download[0], args.download[1])
            else:
                downloadGameLogs(robot, args.download[0], args.download[1])
      
        else:
            print ("no command specified")
   
            
