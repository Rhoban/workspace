import tempfile
import os
import time
from colorama import Fore, Back, Style
import subprocess

def success(message: str):
    """
    Displays a message in a success fashion

    :param str message: the message
    """
    print("")
    print(Style.BRIGHT + Fore.GREEN + message + Style.RESET_ALL)


def warning(message: str):
    """
    Displays a message in a warning fashion

    :param str message: the message
    """
    print("")
    print(Style.BRIGHT + Fore.YELLOW + message + Style.RESET_ALL)


def error(message: str):
    """
    Displays a message in a error fashion

    :param str message: the message
    """
    print("")
    print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)


def bright(message: str):
    """
    Displays a message in a bright fashion

    :param str message: the message
    """
    print(Style.BRIGHT + message + Style.RESET_ALL)


def question_answers(question: str, answers: list, default: str = "") -> str:
    """
    Asks a question and expect one of the given answers

    :param str question: askes question
    :param dict answers: possible answers
    :return str: given answer
    """
    possibilities = ",".join(answers)

    if default != "":
        possibilities += f" [{default}]"

    while True:
        print("")
        answer = input(Style.BRIGHT + f"{question} ({possibilities}): " + Style.RESET_ALL).strip()

        if answer == "":
            answer = default

        if answer in answers:
            return answer
        else:
            warning(f"Possible answers are: {possibilities}" + Fore.RESET)


def yes_no(question: str, default: str = "") -> bool:
    """
    Asks a yes/no question

    :param str question: Question to ask
    :param str default: default value (yes or no)
    :return bool: True if yes elese no
    """
    return question_answers(question, ["y", "n"], default) == "y"


def rhio(hostname: str, command: str) -> str:
    """
    Sends a rhio command to a given host and returns its result

    :param str hostname: remote hostname
    :param str command: command to execute
    :return str: the command result
    """
    return subprocess.check_output(["rhio", hostname, *command.split(" ")]).decode("utf-8").strip()


def rhio_get_value(hostname: str, node: str) -> str:
    """
    Gets a value from RhIO

    :param str hostname: the remote host
    :param str node: the node name (ex: /referee/teamId)
    :return str: the value
    """
    return "=".join(rhio(hostname, node).split("=")[1:])

def rhio_commands(hostname: str, commands: str) -> None:
    """
    Execute some commands in batch

    :param str hostname: the remote host
    :param str commands: list of commands
    """    
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(commands.encode("utf-8"))
    tmpfile.flush()

    os.system(f"rhio {hostname} < {tmpfile.name}")

