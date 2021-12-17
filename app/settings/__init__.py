import os
from .base import REPO_DIR, config as base_config
from .product import config as product_config

_AG_DEBUG = os.environ.get("AG_DEBUG", "true")
if _AG_DEBUG == "true":
    AG_DEBUG = True

if AG_DEBUG:
    config = base_config
else:
    config = product_config
