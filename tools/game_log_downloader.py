#!/usr/bin/python3

import argparse
import subprocess

def sshCmd(robot_no, cmd, timeout = 3):
    """
    Execute the requested command on the given robot and returns the output of the process
    Raise a RuntimeError if ssh command failed
    """
    robot_ip = "rhoban@10.2.0." + str(100 + robot_no)
    result = subprocess.run(["ssh","-o ConnectTimeout=3", robot_ip, cmd],
                            stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out_str = result.stdout.decode("ascii").strip()
    if result.returncode == 0:
        return out_str
    else:
        raise RuntimeError("ssh exit with code " + str(result.returncode) + ": " + out_str
                           + "(cmd: '" + cmd + "' failed)")

def checkFolder(robot_no, path):
    """
    Raise a RuntimeError if folder 'path' on 'robot_no' does not exist
    """
    sshCmd(robot_no, "[ -d " + path + " ]")

def getRobotName(robot_no):
    """
    Raise a RuntimeError if it fails to retrieve the hostname
    """
    return sshCmd(robot_no, "hostname")

def downloadGameLogs(robot_no, game_log_path, dst):
    """
    Download the log at given robot_log_path from robot_no to the target folder.
    The perception logs and lowlevel logs are separated in two different folders.
    """
    # Getting name + preparing folder names
    robot_name = getRobotName(robot_no)
    team_id = "team9"
    robot_path = dst + "/" + team_id + "/" + robot_name
    perception_path = robot_path + "/perception"
    log_path = robot_path + "/log"
    compress_target="game_logs.tar.gz"
    # Checking that folder exists
    print("Checking existence of folder '" + game_log_path + "' on robot")
    checkFolder(robot_no, path)
    # Compressing file
    print("Compressing folder on robot")
    sshCmd(robot_no, "tar -cvzf " + compress_target + " " + game_log_path)
    

def listGameLogs(robot_no):
    return sshCmd(robot_no, "find . -name \"game_logs\" | xargs du -hs | sort -h")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd = parser.add_mutually_exclusive_group()
    cmd.add_argument("-l", "--list", action="store_true",
                     help="List the game logs available on the robot")
    cmd.add_argument("-c", "--check", type=str, metavar="PATH",
                     help="Check if a log exist")
    cmd.add_argument("-d", "--download", type=str, nargs=2, metavar="LOG_PATH DST_PATH",
                     help="Download a log from LOG_PATH to the folder DST_PATH")
    parser.add_argument("robot_no", type=int,help="robot id [1-...]")
    args = parser.parse_args()
    robot_no = args.robot_no
    if args.list:
        print(listGameLogs(robot_no))
    elif args.check:
        checkFolder(robot_no,args.check)
    elif args.download:
        downloadGameLogs(robot_no, args.download[0], args.download[1])
    else:
        print ("no command specified")
