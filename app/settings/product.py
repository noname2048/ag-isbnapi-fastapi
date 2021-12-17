from app.settings.base import REPO_DIR
import os
from dotenv import dotenv_values

if os.path.isdir(REPO_DIR / ".env"):
    raise EnvironmentError(".env file and os environment are both exist!")

config = {**os.environ}
