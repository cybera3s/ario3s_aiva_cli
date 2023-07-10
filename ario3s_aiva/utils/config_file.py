from pathlib import Path
import tomli
from typing import Any
import typer
import sys
from rich import print

# Local imports
from ario3s_aiva.config import CONFIG_FILE


def is_config_file_exist() -> bool:
    """
    Check if config file exists

    True if exists else False
    """

    if not CONFIG_FILE.exists():
        return False

    return True


def validate_default_section() -> bool:
    """
    Validates default section of config file
    """

    default = config_default_section()

    if not default["server_label"]:
        return False

    if not default["local_port"]:
        return False

    return True


def check_config_file():
    """
    This functions is used as callback before every command

    Check and validate config file
    """

    if is_config_file_exist():
        if not validate_default_section():
            print("[red bold]Default section " "is not complete!")
            print(
                "[yellow bold]Make sure to provide: 'local_port',"
                " 'username', 'server_label' in default section"
            )
            sys.exit()

    else:
        print(f"[bold red]Config file does not exists at: [/]{CONFIG_FILE}")
        raise typer.Exit()


def read_config_file(
    config_file_path: Path = CONFIG_FILE,
) -> dict[str, Any] | None:
    """
    Reads config file data if exists

    Return:
        (None or dict) config data or None
    """

    if is_config_file_exist():
        with open(config_file_path, "rb") as file:
            return tomli.load(file)

    return None


def config_default_section():
    """
    Returns default section of config file
    """
    return read_config_file()["default"]


def get_default_server_label() -> str:
    """
    Returns default server label from default section
    """
    return config_default_section()["server_label"]


def get_servers_list() -> list:
    """
    Get available servers
    if any else empty list
    """

    sections = read_config_file()
    # filter sections that starts with 'server_'
    filterd_sections = list(
        filter(lambda s: s.startswith("server_"), sections.keys())
    )

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
    return read_config_file().get(section_name)
