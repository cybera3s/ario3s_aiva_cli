import typer
from typing import Any
import tomli
import pathlib
import os
import subprocess
from rich import print
import sys


CURRENT_USER: str = os.getlogin()
CONFIG_FILE: pathlib.Path = pathlib.Path(f"/home/{CURRENT_USER}/.aiva.toml")


# check config file
def get_config() -> dict:
    if not CONFIG_FILE.exists():
        print(f"[bold red]Config file does not exists at [/]{CONFIG_FILE}")
        sys.exit()

    with open(CONFIG_FILE, "rb") as config_file:
        return tomli.load(config_file)


app = typer.Typer(callback=get_config)

# global server config
if get_config():
    print(f"[bold green]Config File Found![/] {CONFIG_FILE}\n")
    server: dict = get_config()["server"]


def get_status() -> int:
    """return status of ssh session"""
    command = f'pgrep -alx ssh | grep {server["username"]}@{server["ip"]}'
    return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


@app.command()
def connect(port: int = 4321):
    """
    connect to server and creates a SOCKS proxy with provided port
    """
    status: int = get_status()

    if status == 0:
        typer.echo("You already have open session, enjoy!")
        raise typer.Exit(code=1)

    connect_command = f'ssh -f -N -D {port} \
        {server["username"]}@{server["ip"]} -p {server["port"]}'

    res: int = subprocess.call(connect_command, shell=True)

    if res == 0:
        typer.echo(f"SOCKS Proxy Successfully created on 127.0.0.1:{port}")


@app.command()
def disconnect():
    """
    disconnect from server by killing ssh process
    """

    if get_status() == 0:
        command: str = f'kill -9 $(pgrep -axl ssh | grep {server["username"]}@{server["ip"]} | cut -d " " -f 1)'
        kill_result: int = subprocess.call(command, shell=True)

        if kill_result == 0:
            typer.echo("Session Closed Successfully!")
    else:
        typer.echo("No Open Session!")


@app.command()
def status(
    detail: bool = typer.Option(
        False, "--detail", "-d", help="Show detail about Connection"
    )
):
    """
    get status of ssh connection
    """
    status_result = get_status()

    if status_result == 0:
        if detail:
            data = subprocess.check_output(PROCESS_INFO_CMD, shell=True).decode()
            connected_port: str = data.split(" ")[5]

            print(f"[blue bold]SOCKS proxy Listening at {connected_port}")

        print("[bold yellow]You have open session!")
    else:
        print("[bold cyan]You are not connected!")
