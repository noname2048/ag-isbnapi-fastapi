from pathlib import Path as SysPath
import os

_FILE_DIR = SysPath(__file__).resolve()
_SETTING_DIR = _FILE_DIR.parent
_APP_DIR = _SETTING_DIR.parent
REPO_DIR = _APP_DIR.parent

if not os.path.isdir(REPO_DIR / "app"):
    raise EnvironmentError
