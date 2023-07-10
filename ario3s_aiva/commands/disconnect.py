# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.run_command import (
    run_disconnect,
    get_ssh_session_status,
)


def disconnect():
    """
    Disconnects from server
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
