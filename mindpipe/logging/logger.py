"""
    Module that contains the logger configuration
"""

import pathlib
import random
import string

from loguru import logger

TMP_FOL = pathlib.Path("/tmp/mindpipe")
TMP_FOL.mkdir(exist_ok=True)
FNAME = "".join(random.choices(string.ascii_lowercase + string.digits, k=16)) + ".log"
TMP_FILE = TMP_FOL / FNAME

CONFIG = {
    "handlers": [
        {
            "sink": str(TMP_FILE),
            "format": "{time:YY-MM-DD at HH:mm:ss} | {level} | {message}",
        }
    ]
}

logger.configure(**CONFIG)
logger.disable("mindpipe")
LOG = logger
