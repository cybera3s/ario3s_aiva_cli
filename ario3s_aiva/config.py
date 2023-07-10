from pathlib import Path
import os


CURRENT_USER: str = os.getlogin()
CONFIG_FILE: Path = Path(f"/home/{CURRENT_USER}/.aiva.toml")
