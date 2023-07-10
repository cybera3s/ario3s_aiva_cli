import subprocess
from subprocess import CompletedProcess
from ario3s_aiva.utils.config_file import (
    get_default_server_label,
    get_server_data,
    config_default_section,
)

from ario3s_aiva.utils.os_commands import (
    find_ssh_process_cmd,
    get_connect_command,
)


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
    command: str = f"kill -9 {pid}"
    return subprocess.run(command, shell=True)


def get_pid_ssh_session():
    """Returns process id of current SSH session"""

    if get_ssh_session_status():
        default_server = get_default_server_label()
        server_info = get_server_data(default_server)

        ip = server_info["ip"]
        bind_port = config_default_section().get("local_port")
        username = config_default_section().get("username")

        find_cmd = find_ssh_process_cmd(bind_port, username, ip)
        result = subprocess.run(
            find_cmd, shell=True, text=True, capture_output=True
        )

        if result.returncode == 0:
            pid = result.stdout.split(" ")[0]
            return pid


def get_ssh_session_status() -> bool:
    """
    Gets status of current ssh session

    Return:
        status (bool): True if ssh session is open otherwise False
    """

    default_server = get_default_server_label()
    server_info = get_server_data(default_server)

    ip = server_info["ip"]
    local_port = config_default_section().get("local_port")
    username = config_default_section().get("username")

    find_command = find_ssh_process_cmd(local_port, username, ip)
    result: CompletedProcess = subprocess.run(
        find_command, shell=True, stdout=subprocess.DEVNULL
    )

    if result.returncode == 0:
        return True
    else:
        return False
