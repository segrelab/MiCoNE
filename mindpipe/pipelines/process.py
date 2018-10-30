"""
    Module that defines different pipeline processes
"""

import collections
import os
import pathlib
import shutil
from typing import Optional
from warnings import warn

import delegator

from .template import ConfigTemplate, ScriptTemplate
from ..config import Params


class Process(collections.Hashable):
    """
        Class for executing pipeline processes

        Parameters
        ----------
        params : Params
            The parameters for a particular process
        profile : {'local', 'sge'}
            The execution environment
        script_name : str, optional
            The name of the process script template
            Default is 'process.nf'
        config_name : str, optional
            The name of the process configuration template
            Default is 'process.config'
        process_dir_name : str, optional
            The name of the process directory where the templates are stored
            Default is 'processes'

        Attributes
        ----------
        name : str
            The name of the process
        params : Params
            The core parameters object for the process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
    """
    _nf_path: pathlib.Path = pathlib.Path(os.environ["NF_PATH"])

    def __init__(
            self,
            params: Params,
            profile: str,
            script_name: str = "process.nf",
            config_name: str = "process.config",
            process_dir_name: str = "processes",
    ) -> None:
        self.params = params
        self.name = self.params.name
        self.profile = profile
        script_file = self.params.root / script_name
        process_dir = self.params.root / process_dir_name
        config_file = self.params.root / config_name
        self.script = ScriptTemplate(script_file, process_dir)
        self.config = ConfigTemplate(config_file)
        self._output_location = self.params.output_location

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Process name={self.name} cmd={self.cmd}>"

    def __str__(self) -> str:
        return self.name

    def build(self, output_dir: Optional[str] = None) -> None:
        """
            Builds the pipeline script and the config file at the output_dir
            Updates the output_location for all the results

            Parameters
            ----------
            output_dir : str, optional
                The directory where the scripts and config files are to be built
                This directory will be also be used to store the results of the process
        """
        if output_dir:
            self._output_location = pathlib.Path(output_dir)
        if not self._output_location.is_absolute() or not self._output_location.exists():
            raise FileNotFoundError(f"{self._output_location} must be an absolute path and must exist")
        script = self.script.render()
        script_file = self._output_location / f"{self.name}.nf"
        # TODO: Add logging here
        with open(script_file, 'w') as fid:
            fid.write(script)
        config = self.config.render(self.params.dict)
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

    def run(self) -> delegator.Command:
        """
            Starts the execution of the process and returns the job id (cluster) or pid (local)

            Returns
            -------
            delegator.Command
                The delegator command object
                It has `cmd`, `out`, `pid` and other facilities
        """
        if self.cmd is None:
            raise ValueError("You must run the `build` method on the instance before execution")
        run_inst = delegator.run(self.cmd, block=False)
        return run_inst

    def clean(self, scope: str) -> None:
        """
            Cleans out the requested scope

            Parameters
            ----------
            scope : {'all', 'work_dir'}
                The scope to be cleaned
        """
        warn("You are about to delete files and folders which is in irreversible process")
        if not self._output_location.is_absolute() or not self._output_location.exists():
            raise FileNotFoundError(f"{self._output_location} does not exist or is not an absolute path")
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

    def attach_to(self, previous: "Process") -> None:
        """
            Update inputs of current `Process` instance using outputs of previous

            Parameters
            ----------
            previous : Process
                The `Process` instance to attach the current instance to
        """
        self.params.attach_to(previous.params)

    def update_location(self, location: str) -> None:
        """
            Update the location of an Input or Output element

            Parameters
            ----------
            location : str
                The location of the IO element
        """
        path = pathlib.Path(location)
        if not path.is_absolute():
            raise ValueError("location must be an absolute path")
        for input_ in self.params.input:
            in_location = input_.location
            if in_location is None:
                raise ValueError("Process parameter inputs are incomplete")
            if not in_location.is_absolute():
                self.params.update_location(input_.datatype, path / in_location, "input")
        for output_ in self.params.output:
            out_location = output_.location
            if out_location is None:
                raise ValueError("Process parameter outputs are incomplete")
            if not out_location.is_absolute():
                self.params.update_location(output_.datatype, path / out_location, "output")


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
        self.env = self.params.env

    def __repr__(self) -> str:
        return f"<ExternalProcess name={self.name} cmd={self.cmd}>"

    def run(self):
        # Source environment before running
        pass
