# Local imports
from ario3s_aiva.commands import print
from ario3s_aiva.utils.run_command import (
    get_ssh_session_status,
    run_disconnect,
    run_connect,
)


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
