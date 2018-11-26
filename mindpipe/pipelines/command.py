"""
    Module that handles the execution of subprocesses and parsing of their outputs
"""

import sys
from typing import List, Optional

import subprocess


class Command:
    """
        Class that wraps functionality for running subprocesses and jobs on the cluster

        Parameters
        ----------
        cmd : str
            The command to be executed
        profile : {'local', 'sge'}
            The execution environment
        timeout : int, optional
            The time limit for the command
            If a process exceeds this time then it will be terminated
            Default is 1000

        Attributes
        ----------
        cmd : str
            The command that will be executed.
            This includes the profile and resource specifics
        profile : {'local', 'sge'}
            The execution environment
        output : str
            The 'stdout' of the process
    """

    _stdout: Optional[str] = None
    _stderr: Optional[str] = None
    process: Optional[subprocess.Popen] = None

    def __init__(self, cmd: str, profile: str, timeout: int = 1000) -> None:
        # TODO: Set up profiles config
        self.profile = profile
        self.cmd = self._build_cmd(cmd)
        self._timeout = timeout

    def _build_cmd(self, cmd: str) -> str:
        """
            Builds the `cmd` for the current Command instance

            Parameters
            ----------
            cmd : str
                The command to be executed

            Returns
            -------
            str
                The final command to be executed
        """
        command: List[str] = []
        if self.profile == "local":
            pass
        elif self.profile == "sge":
            command.append("qsub")
        else:
            raise ValueError("Unsupported profile! Choose either 'local' or 'sge'")
        command.append(cmd)
        final_cmd = " && ".join(command)
        return final_cmd

    def __str__(self) -> str:
        return self.cmd

    def __repr__(self) -> str:
        return f'<Command cmd="{self.cmd}" timeout={self._timeout}>'

    def run(self, cwd: Optional[str] = None) -> subprocess.Popen:
        """
            Executes the command with the correct profile and resources

            Parameters
            ----------
            cwd : str, optional
                The directory in which the command is to be run
                Default is None which uses the current working directory

            Returns
            -------
            int
                The exit status of the command
        """
        # QUESTION: Replace this with asyncio.subprocess.create_subprocess_shell
        self.process = subprocess.Popen(
            self.cmd,
            cwd=cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return self.process

    # TODO: Change the `log_file` to the logger class
    def log(self, log_file: str) -> None:
        """
            Logs the output of the process to the log_file

            Parameters
            ----------
            log_file : str
                The log file to save the output and error to
        """
        if self._stdout is not None and self._stderr is not None:
            stdout = self._stdout
            stderr = self._stderr
        else:
            if self.process:
                stdout, stderr = self.process.communicate(timeout=self._timeout)
                stdout = stdout.decode("utf-8")
                stderr = stderr.decode("utf-8")
            else:
                raise NotImplementedError(
                    "Please run the command before requesting errors!"
                )
        with open(log_file, "w") as fid:
            fid.write("-" * 40 + " [STDOUT] " + "-" * 40)
            fid.write("\n")
            sys.stdout.write(stdout)
            fid.write(stdout)
            fid.write("\n")
            fid.write("-" * 40 + " [STDERR] " + "-" * 40)
            fid.write("\n")
            sys.stderr.write(stderr)
            fid.write(stderr)

    @property
    def output(self) -> str:
        """
            Returns the output generated during execution of the command

            Returns
            -------
            str
                The `stdout` of the process
        """
        if self._stdout is not None:
            stdout = self._stdout
        else:
            if self.process:
                stdout, stderr = self.process.communicate(timeout=self._timeout)
                self._stdout = stdout.decode("utf-8")
                self._stderr = stderr.decode("utf-8")
            else:
                raise NotImplementedError(
                    "Please run the command before requesting output!"
                )
        return self._stdout

    @property
    def error(self) -> str:
        """
            Returns the error generated during execution of the command

            Returns
            -------
            str
                The `stderr` of the process
        """
        if self._stderr is not None:
            stderr = self._stderr
        else:
            if self.process:
                stdout, stderr = self.process.communicate(timeout=self._timeout)
                self._stdout = stdout.decode("utf-8")
                self._stderr = stderr.decode("utf-8")
            else:
                raise NotImplementedError(
                    "Please run the command before requesting errors!"
                )
        return self._stderr

    def update(self, cmd: str) -> None:
        """
            Update the `cmd` of the current Command instance

            Parameters
            ----------
            cmd : str
                The new command to be executed
        """
        self.cmd = self._build_cmd(cmd)


# QUESTION: What should write the profiles and resources `config` files? A new template module?
# Fixes #44
