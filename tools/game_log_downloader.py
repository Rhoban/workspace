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
    perception_path = robot_path + "/perception"
    output_log_path = robot_path + "/output_log"
    print("Checking existence of folder '" + game_log_path + "' on robot")
    checkFolder(host, game_log_path)
    output_logs = game_log_path + "/*.log"
    video_logs = game_log_path + "/*/"
    systemOrRaise(["mkdir", "-p", output_log_path])
    print("Copying output logs from '" + output_logs + "'")
    scpCmd(host, output_logs, output_log_path)
    systemOrRaise(["mkdir", "-p", perception_path])
    print("Copying video logs from '" + video_logs + "'")
    scpCmd(host, video_logs, perception_path)
    #TODO: move folder to tmp/robot_name/perception and tmp/robot_name/output_logs before creating arxiv
    #This part was suited for old logs format (png) but not for new (avi)
    #print("Compressing folder on robot (might last several minutes)")
    #sshCmd(host, "tar -czf " + compress_target + " " + game_log_path)
    #print("Downloading " + compress_target + " from " + robot_name)
    #tmp_local_arxiv = dst + "/" + compress_target
    #scpCmd(host, compress_target, tmp_local_arxiv)
    #print("Extracting data")
    #systemOrRaise(["tar","-xzf ",tmp_local_arxiv])
    #print("Moving data")
    #TODO: move data (require to see/check structure)
    # - Currently all the data are placed in 
    #TODO: clean data

def listGameLogs(host):
    return sshCmd(host, "find . -name \"game_logs\" | xargs du -hs | sort -h")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd = parser.add_mutually_exclusive_group()
    cmd.add_argument("-l", "--list", action="store_true",
                     help="List the game logs available on the robot")
    cmd.add_argument("-c", "--check", type=str, metavar="PATH",
                     help="Check if a log exist")
    cmd.add_argument("-d", "--download", type=str, nargs=2, metavar="LOG_PATH DST_PATH",
                     help="Download a log from LOG_PATH to the folder DST_PATH")
    parser.add_argument("robot", type=str,help="robots hostnames")
    args = parser.parse_args()
    robot = args.robot
    if args.list:
        print(listGameLogs(robot))
    elif args.check:
        checkFolder(robot,args.check)
    elif args.download:
        downloadGameLogs(robot, args.download[0], args.download[1])
    else:
        print ("no command specified")
