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


def get_default_config():
    """
    Returns default section of config file
    """

    return get_config()["default"]


def validate_default_section() -> bool:
    default = get_default_config()

    if not default["server_label"]:
        return False

    if not default["local_port"]:
        return False

    return True


def read_config_data():
    """
    Reads config file data
    """

    # if config file has data
    if get_config():
        print(f"[bold green]Config File Found![/] {CONFIG_FILE}\n")

        if not validate_default_section():
            print("[red bold]Default section is not complete!")
            print(
                "[yellow bold]Make sure to provide: 'local_port', 'username', 'server_label' in default section"
            )
            sys.exit()
    else:
        print("[red bold]Something wrong with config file")


read_config_data()


def get_default_server_label() -> str:
    """
    Returns default server label from default section
    """

    default = get_default_config()
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
    Gets status of current ssh session

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


def get_connect_command(server_info: dict) -> str:
    """
    Get dynamic ssh tunnel command with provided server info data
    """

    ip = server_info["ip"]
    port = server_info["port"]
    bind_port = get_default_config().get("local_port")
    username = get_default_config().get("username")

    command = f"ssh -f -N -D {bind_port} \
        {username}@{ip} -p {port}"

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

    status: int = get_ssh_session_status()

    if status:
        print("[bold cyan]You already have open session, enjoy!")
        raise typer.Exit(code=1)

    else:
        connect_command = get_connect_command()
        conn_result: CompletedProcess = subprocess.run(connect_command, shell=True)

        if conn_result.returncode == 0:
            print(
                f"[bold green]SOCKS Proxy Successfully created on [/]127.0.0.1:{port}"
            )
        else:
            print(f"[bold red]SOCKS Proxy failed to create!")


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
