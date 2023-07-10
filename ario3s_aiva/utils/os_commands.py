from ario3s_aiva.utils.config_file import config_default_section


def get_connect_command(server_info: dict) -> str:
    """
    Get dynamic ssh tunnel command with provided server info data
    """

    ip = server_info["ip"]
    port = server_info["port"]
    bind_port = config_default_section().get("local_port")
    username = config_default_section().get("username")

    command = f"ssh -f -N -D {bind_port} \
        {username}@{ip} -p {port}"

    return command


def find_ssh_process_cmd(bind_port: str, username: str, ip: str) -> str:
    """
    Returns find dynamic ssh tunnel process with provided data
    """

    return f'pgrep -alx ssh | grep "D {bind_port} {username}@{ip}"'
