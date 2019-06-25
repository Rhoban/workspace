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
    print("Checking existence of folder '" + game_log_path + "' on robot")
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
    parser.add_argument("-m", "--manual", action="store_true",
                        help="Focus on manual logs")
    parser.add_argument("robot", type=str,help="robots hostnames")
    args = parser.parse_args()
    robot = args.robot
    if args.list:
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
