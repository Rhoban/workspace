#!/usr/bin/env python3

import subprocess
import sys

default_host = "10.0.0.1"

TM_RED = '\033[91m'
TM_BOLD = '\033[1m'
TM_UNDERLINE = '\033[4m'
TM_END = '\033[0m'

def systemOrRaise(args):
    """
    Execute a system command and raise a RuntimeError on failure.
    Input/output is captured and output is returned.
    """
    result = subprocess.run(args, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out_str = result.stdout.decode("ascii").strip()
    if result.returncode == 0:
        return out_str
    else:
        raise RuntimeError("Failed to execute system '" + str(args) + "' output: " + out_str)

def sshCmd(host, cmd, timeout = 3):
    """
    Execute the requested command on the given robot and returns the output of the process
    Raise a RuntimeError if ssh command failed
    """
    return systemOrRaise(["ssh","-o ConnectTimeout=3", "rhoban@" + host, cmd])

def scpCmd(host, robot_path, local_path):
    """
    Execute the requested command on the given robot and returns the output of the process
    Raise a RuntimeError if ssh command failed
    """
    systemOrRaise(["scp", "-r", "rhoban@" + host + ":" + robot_path, local_path])

def checkFolder(host, path):
    """
    Raise a RuntimeError if folder 'path' on 'robot_no' does not exist
    """
    sshCmd(host, "[ -d " + path + " ]")

def getRobotName(robot_no):
    """
    Raise a RuntimeError if it fails to retrieve the hostname
    """
    return sshCmd(robot_no, "hostname")
    
def msg(phase, msg):
    print("{:}{:}: {:}{:}\n".format(TM_BOLD,phase, msg, TM_END))

def prompt(phase, message, options):
    while True:
        msg(phase,message)
        print("> ", end='')
        sys.stdout.flush()
        answer = sys.stdin.readline().strip().lower()
        if answer in options:
            return answer
        print("{:}{:}You should answer one of the following: {:}{:}".format(TM_RED,TM_BOLD,options,TM_END))

def question(phrase, message):
    return prompt(phrase, message, ['y', 'n']) == 'y'

def rhioCmd(cmd, host=default_host, display=True):
    result = systemOrRaise(["rhio", host, cmd])
    if display and result != "":
        print(result)
    return result

def isHandled(host):
    return rhioCmd('/decision/handled', host) == "/decision/handled=true"

def requestTare(host = default_host):
    while True:
        msg("TARE", "Hold {:} in the air and press enter".format(host))
        sys.stdin.readline()
        result = rhioCmd("tare", host)
        if "Error" in result:
            if not question(TM_RED + "ERROR", 'Tare returned an error, continue anyway?'):
                continue
        rhioCmd("rhalSaveConf rhal.json", host)
        break
    

def requestGyroTare(host):
    while True:
        msg('GYROTARE', 'Put {:} on the floor now and press enter'.format(host))
        sys.stdin.readline()
        result = rhioCmd('rhalGyroTare', host)
        if "Error" in result:
            if not question(TM_RED + "ERROR", 'GyroTare returned an error, continue anyway?'):
                continue
        rhioCmd('rhalSaveConf rhal.json', host)

        msg('CHECK', 'Checking the pressure')
        if isHandled(host):
            if question(TM_RED + "ERROR", 'Decision said I am handled when I should be on the floor, continue anyway?'):
                break
        else:
            break

def askDouble(msg):
    while True:
        try:
            print("\n{:}\n".format(msg))
            return float(sys.stdin.readline().strip())
        except ValueError as err:
            print(TM_BOLD + TM_RED + str(err) + TM_END)

def defaultInit(host):
    """
    Launches init, walk and perform both tare and gyroTare on given host
    """
    msg('INIT', 'Press enter to run init on ' + host)
    sys.stdin.readline()
    rhioCmd('init', host)
    msg('INIT', 'Press enter to run walk on ' + host)
    sys.stdin.readline()
    rhioCmd('walk', host)
    requestTare(host)
    requestGyroTare(host)

def manualCustomReset(host):
    msg("CUSTOM_RESET", "Performing a manual custom Reset for " + host)
    posX = askDouble("Enter x position [m]:")
    posY = askDouble("Enter y position [m]:")
    direction = askDouble("Enter robot orientation [deg]:")
    cmd = "customReset {:} {:} {:} 0.05 0.005".format(posX,posY,direction)
    rhioCmd(cmd, host)


# A few basic tests if runned alone
if __name__ == "__main__":
    prompt("TEST", "What do you prefer", ["apples", "pears", "banana"])
    while not question("TEST", "Would you like to stop"):
        msg("TEST", "repeating")
    number = askDouble("Enter a number")
    msg("TEST", "Number entered is {:}".format(number))
