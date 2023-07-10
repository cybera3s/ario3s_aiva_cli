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


def get_default_config():
    """
    Returns default section of config file
    """

    return get_config()["default"]


def validate_default_section():
    default = get_default_config()

    if not default["server_label"]:
        print("[red bold]'server_label' is not present in default section")


def get_default_server_label() -> str:
    """
    Returns default server label from default section
    """

    default = get_default_config
    return default["server_label"]


def get_servers_list() -> list:
    """
    Get available servers
    if any else empty list
    """

    sections = get_config()
    # filter sections that starts with 'server_'
    filterd_sections = list(filter(lambda s: s.startswith("server_"), sections.keys()))

    if len(filterd_sections) > 0:
        return list(map(lambda server: server.split("_")[1], filterd_sections))
    else:
        return []


def get_server_data(server_label: str) -> dict | None:
    """
    Returns server information
    if server does not exists returns None

    (dict or None) server info
    {
        "ip": IP,
        "port": PORT,
        ...
    }
    """

    section_name = f"server_{server_label}"
    return get_config().get(section_name)


def find_ssh_process_cmd(bind_port: str, username: str, ip: str) -> str:
    """
    Returns find dynamic ssh tunnel process with provided data
    """

    return f'pgrep -alx ssh | grep "D {bind_port} {username}@{ip}"'


def get_ssh_session_status() -> bool:
    """
    Gets status of ssh session

    Return:
        status (bool): True if ssh session is open otherwise False
    """

    default_server = get_default_server_label()
    server_info = get_server_data(default_server)

    ip = server_info["ip"]
    local_port = get_default_config().get("local_port")
    username = get_default_config().get("username")

    find_command = find_ssh_process_cmd(local_port, username, ip)
    result: CompletedProcess = subprocess.run(
        find_command, shell=True, stdout=subprocess.DEVNULL
    )

    if result.returncode == 0:
        return True
    else:
        return False


def get_connect_command() -> str:
    """
    Get ssh tunnel dynamic command
    """

    command = f'ssh -f -N -D {server["local_port"]} \
        {server["username"]}@{server["ip"]} -p {server["server_port"]}'

    return command


@app.command(name="servers_list", help="Get list of available servers")
def list_servers():
    """
    Get servers list
    """

    servers: list = get_servers_list()

    print("[green]Available Servers:")

    for index, server in enumerate(servers, start=1):
        print(f"{index}- {server}")


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
