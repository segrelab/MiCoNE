"""
    Module that defines different pipeline processes
"""

import collections
import os
import pathlib
import shutil
from typing import Optional
from warnings import warn

from .template import ConfigTemplate, ScriptTemplate
from ..config import Params


class Process(collections.Hashable):
    """
        Class for executing pipeline processes

        Parameters
        ----------
        params : Params
            The parameters for a particular process

        Attributes
        ----------
        name : str
            The name of the process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
    """
    _nf_path: pathlib.Path = pathlib.Path(os.environ["NF_PATH"])

    def __init__(self, params: Params) -> None:
        self._params = params
        self.name = self._params.name
        script_file = self._params.root / "process.nf"
        process_dir = self._params.root / "process"
        config_file = self._params.root / "process.config"
        self.script = ScriptTemplate(script_file, process_dir)
        self.config = ConfigTemplate(config_file)
        self._output_location = self._params.output_location

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Process name={self.name} cmd={self.cmd}>"

    def __str__(self) -> str:
        return self.name

    def build(self, output_dir: Optional[str] = None) -> None:
        """
            Builds the pipeline script and the config file at the output_dir
            Also updates the `cmd` attribute of the instance

            Parameters
            ----------
            output_dir : str, optional
        """
        if output_dir:
            self._output_location = pathlib.Path(output_dir)
        if not self._output_location.exists():
            raise FileNotFoundError(f"{self._output_location} must exist before process can be built")
        script = self.script.render()
        script_file = self._output_location / f"{self.name}.nf"
        # TODO: Add logging here
        with open(script_file, 'w') as fid:
            fid.write(script)
        config = self.config.render(self._params.dict)
        config_file = self._output_location / f"{self.name}.config"
        with open(config_file, 'w') as fid:
            fid.write(config)

    @property
    def cmd(self) -> Optional[str]:
        """
            The command that will be executed for running the process

            Returns
            -------
            Optional[str]
                The command to be executed
                Returns None if build has not been run
        """
        script_path = self._output_location / f"{self.name}.nf"
        config_path = self._output_location / f"{self.name}.config"
        work_dir = self._output_location / "work"
        if not script_path.exists() or not config_path.exists() or not work_dir.exists():
            warn("The process has not been built yet. Please run `build` before `run`")
        return f"{self._nf_path} {script_path} -c {config_path} -w {work_dir}"

    def run(self) -> str:
        """
            Starts the execution of the process and returns the job id (cluster) or pid (local)

            Returns
            -------
            str
                The job-id (cluster) or pid (local)
        """
        if self.cmd is None:
            raise ValueError("You must run the `build` method on the instance before execution")
        # TODO: Use delegator

    def clean(self, scope: str) -> None:
        """
            Cleans out the requested scope

            Parameters
            ----------
            scope : {'all', 'work_dir'}
                The scope to be cleaned
        """
        warn("You are about to delete files and folders which is in irreversible process")
        script_path = self._output_location / f"{self.name}.nf"
        config_path = self._output_location / f"{self.name}.config"
        work_dir = self._output_location / "work"
        if scope == "all":
            shutil.rmtree(work_dir)
            script_path.unlink()
            config_path.unlink()
        elif scope == "work_dir":
            shutil.rmtree(work_dir)
        else:
            raise ValueError("Unsupported scope. Please choose from {'all', 'work_dir'}")


class InternalProcess(Process):
    """
        Class for executing an internal pipeline process

        Parameters
        ----------
        params : Params
            The parameters for a particular internal process

        Attributes
        ----------
        name : str
            The name of the internal process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
    """

    def __init__(self, params: Params) -> None:
        super().__init__(params)

    def __repr__(self) -> str:
        return f"<InternalProcess name={self.name} cmd={self.cmd}>"


class ExternalProcess(Process):
    """
        Class for executing an external pipeline process

        Parameters
        ----------
        params : Params
            The parameters for a particular external process

        Attributes
        ----------
        name : str
            The name of the external process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
        env : pathlib.Path
            The location of the virtual environment
    """

    def __init__(self, params: Params) -> None:
        super().__init__(params)

    def __repr__(self) -> str:
        return f"<ExternalProcess name={self.name} cmd={self.cmd}>"

    def run(self):
        # Source environment before running
        pass
