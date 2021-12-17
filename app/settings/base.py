from pathlib import Path as SysPath
import os
from dotenv import dotenv_values

_FILE_DIR = SysPath(__file__).resolve()
_SETTING_DIR = _FILE_DIR.parent
_APP_DIR = _SETTING_DIR.parent
REPO_DIR = _APP_DIR.parent

if not os.path.isdir(REPO_DIR / "app"):
    raise EnvironmentError

config = dotenv_values(REPO_DIR / ".env")
