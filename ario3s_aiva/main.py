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


def get_pid_ssh_session():
    """Returns process id of current SSH session"""

    if get_ssh_session_status():
        default_server = get_default_server_label()
        server_info = get_server_data(default_server)

        ip = server_info["ip"]
        bind_port = get_default_config().get("local_port")
        username = get_default_config().get("username")

        find_cmd = find_ssh_process_cmd(bind_port, username, ip)
        result = subprocess.run(find_cmd, shell=True, text=True, capture_output=True)

        if result.returncode == 0:
            pid = result.stdout.split(" ")[0]
            return pid

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


def run_connect() -> CompletedProcess:
    """
    Runs connect command
    
    Return:
        (CompletedProcess) result of connect command
    """

    label = get_default_server_label()
    default_server_info = get_server_data(label)
    connect_command = get_connect_command(default_server_info)
    return subprocess.run(connect_command, shell=True)


def run_disconnect() -> CompletedProcess:
    """
    Runs disconnect command

    Return:
        (CompletedProcess) result of disconnect command
    """

    pid = get_pid_ssh_session()
    command: str = f'kill -9 {pid}'
    return subprocess.run(command, shell=True)


############# Commands #############

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
        connect_result: CompletedProcess = run_connect()

        if connect_result.returncode == 0:

            bind_port = get_default_config().get("local_port")

            print(
                f"[bold green]SOCKS Proxy Successfully created on [/]127.0.0.1:{bind_port}"\
            )
        else:
            print(f"[bold red]SOCKS Proxy failed to create!")


@app.command()
def disconnect():
    """
    disconnect from server by killing ssh process
    """

    status: int = get_ssh_session_status()

    if status:
        kill_result = run_disconnect()

        if kill_result.returncode == 0:
            print("[green]SSH session Closed Successfully!")
        else:
            print("[red]Something went wrong with closing SSH session!")
    else:
        print("[bold red]No Open Session!")


@app.command()
def status(
    detail: bool = typer.Option(
        False, "--detail", "-d", help="Show detail about Connection"
    )
):
    """
    get status of ssh connection
    """
    status: int = get_ssh_session_status()

    if status:

        if detail:
            bind_port = get_default_config().get("local_port")
            server_label = get_default_config().get("server_label")
            ip = get_server_data(server_label)['ip']

            print(f"[blue bold]SOCKS proxy Listening at: {bind_port}")
            print(f"[blue bold]Server label: {server_label}")
            print(f"[blue bold]Server IP: {ip}")

        print("[bold green]You have open session!")

    else:
        print("[bold cyan]You are not connected!")


@app.command()
def restart():
    """
    Restarts the session
    """

    status: int = get_ssh_session_status()

    # Open ssh session
    if status:
        
        # kill old one
        disconnect_result = run_disconnect()

        if disconnect_result.returncode == 0:
            connect_result = run_connect()

            if connect_result.returncode == 0:
                print("[green bold]Session Restarted Successfully!")

    # No open ssh
    else:
        print("[blue bold]No Open SSH Session!")
