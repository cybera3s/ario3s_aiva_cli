# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.config_file import get_servers_list


def list_servers():
    """
    Get servers list
    """

    servers: list = get_servers_list()

    print("[green]Available Servers:")

    for index, server in enumerate(servers, start=1):
        print(f"{index}- {server}")
