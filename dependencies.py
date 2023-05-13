import os
import subprocess
from rich.console import Console
import requests

from utility import is_valid_wp_login_url

console = Console()


def checkDependencies():
    problems = False

    try:
        devnull = open(os.devnull)
        subprocess.Popen(["ettercap", "--version"], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        console.log(
            f"[red bold]Error:[/red bold] Ettercap not present, install it with the command: sudo apt-get install -y ettercap-graphical")
        problems = True

    try:
        devnull = open(os.devnull)
        subprocess.Popen(["wpbiff", "--version"], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        console.log(
            f"[red bold]Error:[/red bold] Wpbiff not present, install it with the command: pip install wpbiff")
        problems = True

    return not problems


'''
    p = subprocess.Popen(["pip3", "show", "typer"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if "not found" in str(p):
        console.log(
            f"[red bold]Error:[/red bold] Typer not present, install it with the command: pip3 install typer")
        problems = True

    p = subprocess.Popen(["pip3", "show", "rich"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if "not found" in str(p):
        console.log(f"[red bold]Error:[/red bold] Rich not present, install it with the command: pip3 install rich")
        problems = True

    p = subprocess.Popen(["pip3", "show", "pyfiglet"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).communicate()
    if "not found" in str(p):
        console.log(
            f"[red bold]Error:[/red bold] Pyfiglet not present, install it with the command: pip3 install pyfiglet")
        problems = True

    p = subprocess.Popen(["pip3", "show", "termcolor"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).communicate()
    if "not found" in str(p):
        console.log(
            f"[red bold]Error:[/red bold] Termcolor not present, install it with the command: pip3 install termcolor")
        problems = True

    p = subprocess.Popen(["pip3", "show", "pexpect"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).communicate()
    if "not found" in str(p):
        console.log(
            f"[red bold]Error:[/red bold] Pexpect not present, install it with the command: pip3 install pexpect")
        problems = True
'''


def checkServer(server):
    if not is_valid_wp_login_url(server):
        console.log(f"[red bold]URL {server} is not valid!")
        return False
    error = False
    try:
        requests.get(f"{server}")
    except requests.ConnectionError:
        console.log(f"[red bold]404 Server Error:[/red bold] Not Found for url: {server}")
        error = True
    return not error


def checkErrors(server):
    with console.status("Loading..."):
        return checkDependencies() & checkServer(server)
