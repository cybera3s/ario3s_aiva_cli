from typer import Option

# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.run_command import get_ssh_session_status
from ario3s_aiva.utils.config_file import (
    config_default_section,
    get_server_data,
)


def status(
    detail: bool = Option(
        False, "--detail", "-d", help="Show detail about Connection"
    )
):
    """
    get status of ssh connection
    """
    status: int = get_ssh_session_status()

    if status:
        if detail:
            bind_port = config_default_section().get("local_port")
            server_label = config_default_section().get("server_label")
            ip = get_server_data(server_label)["ip"]

            print(f"SOCKS proxy Listening at: [blue bold]{bind_port}")
            print(f"Server label: [blue bold]{server_label}")
            print(f"Server IP: [blue bold]{ip}")

        print("\n[bold green]You have open session!")

    else:
        print("[bold cyan]You are not connected!")
