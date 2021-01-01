"""
    Module that contains the logger configuration
"""

import pathlib
import random
import string

from loguru import logger

TMP_FOL = pathlib.Path("/tmp/micone")
TMP_FOL.mkdir(exist_ok=True)


class Log:
    """
    Class that handles the logging
    Wrapper around `loguru.logger`

    Parameters
    ----------
    folder : pathlib.Path
        Path to the folder containing the log files
        The folder must already exist
    format_str : str
        Format string for the log file
        "timestamp | level | message"
    disable : bool
        Flag to disable logging at the start
        Default value is True

    Attributes
    ----------
    path : pathlib.Path
        The path to the log file
    config : dict
        The dictionary used to configure the `loguru.logger`
    logger : loguru.logger
        The main logging object
    """

    def __init__(
        self, folder: pathlib.Path, format_str: str, disable: bool = True
    ) -> None:
        fname = (
            "".join(random.choices(string.ascii_lowercase + string.digits, k=16))
            + ".log"
        )
        self._folder = folder
        self.path = folder / fname
        self.config = {"handlers": [{"sink": str(self.path), "format": format_str}]}
        logger.configure(**self.config)
        self.logger = logger
        if disable:
            self.logger.disable("micone")

    def enable(self) -> None:
        """ Enable logging """
        self.logger.enable("micone")

    def cleanup(self, nfiles: int = 20) -> None:
        """
        Delete old logs if number > nfiles

        Parameters
        ----------
        nfiles : int
            The threshold for number of log files beyond which the older ones are deleted
            Default value is 10
        """
        log_files = list(self._folder.glob("*.log"))
        log_files_srtd = sorted(
            log_files, key=lambda x: x.stat().st_mtime, reverse=True
        )
        log_files_remove = log_files_srtd[nfiles:]
        for file in log_files_remove:
            file.unlink()


LOG = Log(TMP_FOL, format_str="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
