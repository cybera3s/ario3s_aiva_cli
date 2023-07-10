import typer
import tomli
import pathlib
import os
import subprocess
from subprocess import CompletedProcess
from rich import print
import sys


CURRENT_USER: str = os.getlogin()
CONFIG_FILE: pathlib.Path = pathlib.Path(f"/home/{CURRENT_USER}/.aiva.toml")


# Get config file
def get_config() -> dict:
    """
    Get config file data
    if exists
    """

    if not CONFIG_FILE.exists():
        print(f"[bold red]Config file does not exists at [/]{CONFIG_FILE}")
        sys.exit()

    with open(CONFIG_FILE, "rb") as config_file:
        return tomli.load(config_file)


app = typer.Typer(callback=get_config)

# global server config
if get_config():
    print(f"[bold green]Config File Found![/] {CONFIG_FILE}\n")
    servers: dict = get_config()


def get_process_info_cmd():
    """
    Get process id with its info
    """

    PROCESS_INFO_CMD: str = f'pgrep -alx ssh | grep "D {server["local_port"]} {server["username"]}@{server["ip"]}"'
    return PROCESS_INFO_CMD


def get_status() -> int:
    """
    Get Status of ssh session

    Return:
        0 or greater than zero
        0 means already have a open ssh
        more than zero means no ssh session
    """

    return subprocess.call(PROCESS_INFO_CMD, shell=True, stdout=subprocess.DEVNULL)


def get_connect_command() -> str:
    """
    Get ssh tunnel dynamic command
    """

    command = f'ssh -f -N -D {server["local_port"]} \
        {server["username"]}@{server["ip"]} -p {server["server_port"]}'

    return command


def get_servers_list() -> list:
    """
    Get available servers
    """

    sections = get_config()
    return list(filter(lambda s: s.startswith("server"), sections.keys()))


def get_default_server_label():
    default = get_config()['default']
    return default['server_label']


@app.command(name="servers_list", help="Get list of available servers")
def list_servers():
    """
    Get servers list
    """

    servers: list = get_servers_list()

    print("[green]Available Servers:")

    for index, server in enumerate(servers, start=1):
        print(f"{index}- {server.split('_')[1]}")


@app.command()
def connect():
    """
    Connect to server and creates a SOCKS proxy
    """

    status: int = get_status()

    if status == 0:
        print("[bold cyan]You already have open session, enjoy!")
        raise typer.Exit(code=1)

    connect_command = f'ssh -f -N -D {port} \
        {server["username"]}@{server["ip"]} -p {server["server_port"]}'

    res: int = subprocess.call(connect_command, shell=True)

    if res == 0:
        print(f"[bold green]SOCKS Proxy Successfully created on [/]127.0.0.1:{port}")


# @app.command()
# def disconnect():
#     """
#     disconnect from server by killing ssh process
#     """

#     if get_status() == 0:
#         command: str = f'kill -9 $({PROCESS_INFO_CMD} | cut -d " " -f 1)'
#         kill_result: int = subprocess.call(command, shell=True)

#         if kill_result == 0:
#             typer.echo("Session Closed Successfully!")
#     else:
#         typer.echo("No Open Session!")


# @app.command()
# def status(
#     detail: bool = typer.Option(
#         False, "--detail", "-d", help="Show detail about Connection"
#     )
# ):
#     """
#     get status of ssh connection
#     """
#     status_result = get_status()

#     if status_result == 0:
#         if detail:
#             data = subprocess.check_output(PROCESS_INFO_CMD, shell=True).decode()
#             connected_port: str = data.split(" ")[5]

#             print(f"[blue bold]SOCKS proxy Listening at {connected_port}")

#         print("[bold yellow]You have open session!")
#     else:
#         print("[bold cyan]You are not connected!")


# @app.command()
# def restart():
#     """
#     Restarts the session
#     """

#     # Open ssh session
#     if get_status() == 0:
#         # kill old one

#         command: str = f'kill -9 $({PROCESS_INFO_CMD} | cut -d " " -f 1)'
#         kill_result: int = subprocess.call(command, shell=True)

#         if kill_result == 0:
#             print("[red bold]Session Closed Successfully!")

#         connect_command = get_connect_command()
# mand()
# def disconnect():
#     """
#     disconnect from server by killing ssh process
#     """

#     if get_status() == 0:
#         command: str = f'kill -9 $({PROCESS_INFO_CMD} | cut -d " " -f 1)'
#         kill_result: int = subprocess.call(command, shell=True)

#         if kill_result == 0:
#             typer.echo("Session Closed Successfully!")
#     else:
#         typer.
#     kill_result: CompletedProcess = subprocess.run(connect_command, shell=True)

#     # if
#     if kill_result.returncode == 0:
#         print(
#             f"[bold green]SOCKS proxy successfully created"\
#             f"\nAddress: [/]127.0.0.1:{server['local_port']}"
#         )

# # No open ssh
# else:
#     print("[blue bold]No Open SSH Session!")
