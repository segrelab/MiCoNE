"""
    Module that contains the logger configuration
"""

from loguru import logger

CONFIG = {
    "handlers": [
        {
            "sink": "mindpipe.log",
            "format": "{time:YY-MM-DD at HH:mm:ss} | {level} | {message}",
        }
    ]
}

logger.configure(**CONFIG)
logger.disable("mindpipe")
LOG = logger
