from subprocess import CompletedProcess
import typer

# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.run_command import get_ssh_session_status, run_connect
from ario3s_aiva.utils.config_file import config_default_section


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
            bind_port = config_default_section().get("local_port")

            print(
                "[bold green]SOCKS proxy successfully "
                f"created on [/]127.0.0.1:{bind_port}"
            )
        else:
            print("[bold red]SOCKS Proxy failed to create!")
