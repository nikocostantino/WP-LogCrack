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


def checkServer(server):
    if not is_valid_wp_login_url(server):
        console.log(f"[red bold]URL {server} is not valid!")
        return False
    error = False
    try:
        requests.get(f"{server}", timeout=5)
    except requests.ConnectionError or requests.exceptions.RequestException:
        console.log(f"[red bold]404 Server Error:[/red bold] Not Found for url: {server}")
        error = True
    except requests.exceptions.Timeout:
        console.log(f"[red bold]404 Server Error:[/red bold] Connection timeout expired for url: {server}")
        error = True
    return not error


def checkErrors(server):
    with console.status("Loading..."):
        return checkDependencies() and checkServer(server)
