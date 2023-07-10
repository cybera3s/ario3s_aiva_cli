from rich.prompt import IntPrompt
import typer
import toml

# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.config_file import (
    get_servers_list,
    read_config_file,
)
from ario3s_aiva.config import CONFIG_FILE
from ario3s_aiva.utils.run_command import (
    get_ssh_session_status,
    run_disconnect,
)


def change_server():
    """
    Change default server
    """

    servers = get_servers_list()

    for index, server in enumerate(servers, start=1):
        print(f"{index} - {server}")

    choosed = IntPrompt.ask(
        "\nSelect a server",
        choices=[str(i) for i in range(1, len(servers) + 1)],
    )

    label = servers[choosed - 1]

    data = read_config_file()
    before = data["default"]["server_label"]

    if label == before:
        print(f"\n[bold red]Server is already '{label}'")
        raise typer.Abort()

    data["default"]["server_label"] = label
    after = data["default"]["server_label"]

    status: int = get_ssh_session_status()

    # disconnect if there is open session
    if status:
        print("\n[orange4]There is a open session!")

        disconnect_result = run_disconnect()
        if disconnect_result.returncode == 0:
            print("[bold green]Disconnected Successfully!")
        else:
            print("[bold red]Failed to Disconnect server!")
            raise typer.Exit(1)

    # Save config data
    with open(CONFIG_FILE, "w") as file:
        toml.dump(data, file)

    print(
        f"\n[green]Default server changed from "
        f"[bold blue]'{before}'[/bold blue] "
        f"to [bold yellow]'{after}'[/bold yellow] successfully."
    )
