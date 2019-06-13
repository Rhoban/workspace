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
    if display:
        print(result)
    return result

def isHandled(host):
    return rhioCmd('/decision/handled', host) == "/decision/handled=true"

def requestTare(host = default_host):
    msg("TARE", "Hold me in the air and press enter")
    sys.stdin.readline()
    rhioCmd("tare", host)
    rhioCmd("rhalSaveConf rhal.json", host)
    

def requestGyroTare():
    while True:
        msg('GYROTARE', 'Put me on the floor now and press enter')
        sys.stdin.readline()
        rhioCmd('rhalGyroTare', host)
        rhioCmd('rhalSaveConf rhal.json', host)

        msg('CHECK', 'Checking the pressure')
        if isHandled(host):
            if question("\e[31mERROR", 'Decision said I am handled when I should be on the floor, continue anyway?'):
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
    msg('INIT', 'Press enter to run init')
    sys.stdin.readline()
    rhioCmd('init', host)
    msg('INIT', 'Press enter to run walk')
    sys.stdin.readline()
    rhioCmd('walk', host)
    requestTare(host)
    requestGyroTare(host)

def manualCustomReset(host):
    msg("CUSTOM_RESET", "Performing a manual custom Reset")
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
