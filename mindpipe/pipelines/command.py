"""
    Module that handles the execution of subprocesses and parsing of their outputs
"""

import pathlib
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
        env : str, optional
            The environment to be loaded before execution
            Default is None
        timeout : int, optional
            The time limit for the command
            If a process exceeds this time then it will be terminated
            Default is 1000

        Attributes
        ----------
        cmd : str
            The command that will be executed.
            This includes the environment loading and profile specifics
        output : str
            The 'stdout' of the process
    """
    _stdout: Optional[str] = None
    _stderr: Optional[str] = None

    def __init__(
            self,
            cmd: str,
            profile: str,
            env: Optional[pathlib.Path] = None,
            timeout: int = 1000
    ) -> None:
        # TODO: Set up profiles config
        command: List[str] = []
        if profile == "local":
            pass
        elif profile == "sge":
            pass
        else:
            raise ValueError("Unsupported profile! Choose either 'local' or 'sge'")
        # TODO: Might want to integrate conda with nextflow instead of this
        if env:
            command.append(f"source activate {env}")
        command.append(cmd)
        self.cmd = " && ".join(command)
        self._timeout = timeout

    def run(self, cwd: Optional[str] = None) -> subprocess.Popen:
        """
            Executes the command with the correct environment and resources

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
            stdout, stderr = self.process.communicate(timeout=self._timeout)
        with open(log_file, 'w') as fid:
            fid.write('-' * 40 + " [STDOUT] " + '-' * 40)
            fid.write('\n')
            sys.stdout.write(stdout)
            fid.write(stdout)
            fid.write('\n')
            fid.write('-' * 40 + " [STDERR] " + '-' * 40)
            fid.write('\n')
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
            try:
                stdout, stderr = self.process.communicate(timeout=self._timeout)
                self._stdout = stdout
                self._stderr = stderr
            except AttributeError:
                raise NotImplementedError("Please run the command before requesting output!")
        return stdout

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
            try:
                stdout, stderr = self.process.communicate(timeout=self._timeout)
                self._stdout = stdout
                self._stderr = stderr
            except AttributeError:
                raise NotImplementedError("Please run the command before requesting errors!")
        return stderr

# QUESTION: What should write the profiles and resources `config` files? A new template module?
# Fixes #44