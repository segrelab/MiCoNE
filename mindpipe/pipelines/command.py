"""
    Module that handles the execution of subprocesses and parsing of their outputs
"""

import subprocess
from typing import List, Optional

from ..logging import LOG


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

        Other Parameters
        ----------------
        project : str, optional
            The project under which to run the pipeline on the 'sge'
            Default value is None

        Attributes
        ----------
        cmd : str
            The command that will be executed.
            This includes the profile and resource specifics
        profile : {'local', 'sge'}
            The execution environment
        project : str
            The project under which to run the pipeline on the 'sge'
        output : str
            The 'stdout' of the command
        error : str
            The 'stderr' of the command
        status : str
            The status the the command
            One of {'success', 'failure', 'in progress', 'not started'}
    """

    _stdout: Optional[str] = None
    _stderr: Optional[str] = None
    process: Optional[subprocess.Popen] = None

    def __init__(self, cmd: str, profile: str, timeout: int = 1000, **kwargs) -> None:
        self.profile = profile
        project = kwargs.get("project")
        if profile == "sge":
            if project is None:
                raise ValueError("Project must be supplied if profile is sge")
        self.project = project if project else "None"
        self._cmd = self._build_cmd(cmd)
        self._timeout = timeout

    def _build_cmd(self, cmd: str) -> List[str]:
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
            command.append("-P")
            command.append(self.project)
        else:
            raise ValueError("Unsupported profile! Choose either 'local' or 'sge'")
        command.extend(cmd.split(" "))
        return command

    def __str__(self) -> str:
        return self.cmd

    def __repr__(self) -> str:
        return f'<Command cmd="{self.cmd}" timeout={self._timeout}>'

    @property
    def cmd(self) -> str:
        """ The command that will be executed """
        return " ".join(self._cmd)

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
            self._cmd,
            cwd=cwd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return self.process

    def wait(self) -> None:
        """ Wait for the process to complete or terminate """
        if self.process:
            stdout, stderr = self.process.communicate(timeout=self._timeout)
            self._stderr = stderr.decode("utf-8")
            self._stdout = stdout.decode("utf-8")

    def log(self) -> None:
        """ Logs the stdout and stderr of the command execution to the log_file """
        LOG.logger.info(f"Running command: {self.cmd}")
        LOG.logger.info("-" * 4 + " [STDOUT] " + "-" * 4)
        LOG.logger.success(self.output)
        LOG.logger.info("-" * 4 + " [STDERR] " + "-" * 4)
        LOG.logger.error(self.error)

    def proc_cmd_sync(self) -> bool:
        """
            Check whether the Command instance and subprocess.Popen process are in sync

            Returns
            -------
            bool
                True if both the `cmd` and `process` are the same
        """
        if self._cmd == self.process.args:
            return True
        else:
            return False

    @property
    def output(self) -> str:
        """ Returns the output generated during execution of the command """
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
        """ Returns the error generated during execution of the command """
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
        self._cmd = self._build_cmd(cmd)
        if self.process:
            if not self.proc_cmd_sync():
                LOG.logger.warning(
                    "New command differs from executed command. Clearing previous run"
                )
                self._stdout = None
                self._stderr = None
                self.process = None

    @property
    def status(self) -> str:
        """
            Return the status of the command execution

            Returns
            -------
            str
                One of {'success', 'failure', 'in progress', 'not started'}
        """
        if self.process:
            poll = self.process.poll()
            if poll is None:
                return "in progress"
            if poll == 0:
                return "success"
            if poll > 0:
                return "failure"
            raise RuntimeError("Proces status is undefined")
        else:
            return "not started"
