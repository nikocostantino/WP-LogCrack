import re
import subprocess
from datetime import datetime
import shlex
import subprocess

import tkinter as tk

import pexpect
import typer
from pyfiglet import Figlet
from termcolor import colored
from rich.console import Console


console = Console()

ip_regex = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])$"

url_regex = r"^https?:\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-@?^=%&/~\+#])?\/wp-login\.php$"


def banner():
    f = Figlet(font='standard')
    print(colored(f.renderText('WP-LogCrack'), 'green', attrs=["bold"]))


def handle_sigint(signal, frame):
    console.print("\nApplication terminated by user.", style="bold red underline")
    raise typer.Abort()


def get_timestamp():
    data = datetime.today()
    minute = data.minute
    minute = (minute + 2) % 60
    hour = data.hour
    if minute < 10:
        minute = "0" + str(minute)
    if int(minute) < 40:
        hour = str((data.hour + 1) % 24)
    timestamp = data.strftime('%Y-%m-%d ' + str(hour) + ':' + str(minute))
    return "2023-05-14 14:24"  # timestamp


def is_valid_ip_address(ip):
    if re.match(ip_regex, ip):
        return True
    else:
        return False


def is_valid_wp_login_url(url):
    if re.match(url_regex, url):
        return True
    else:
        return False


def is_pingable(ip_address):
    result = subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0