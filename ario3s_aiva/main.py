import typer

# local imports
from ario3s_aiva.commands import connect
from ario3s_aiva.commands import disconnect
from ario3s_aiva.commands import status
from ario3s_aiva.commands import restart
from ario3s_aiva.commands import list_servers
from ario3s_aiva.utils.config_file import check_config_file


app = typer.Typer(callback=check_config_file)


def define_commands(app):
    """
    Define commands at once
    """
    app.command()(connect.connect)
    app.command()(disconnect.disconnect)
    app.command()(status.status)
    app.command()(restart.restart)
    app.command(name="servers_list", help="Get list of available servers")(
        list_servers.list_servers
    )


define_commands(app)
