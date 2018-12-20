"""
    Module that defines different pipeline processes
"""

import collections
import pathlib
import shutil
from typing import Optional
from warnings import warn

from .command import Command
from .template import ConfigTemplate, ScriptTemplate
from ..config import Params
from ..logging import LOG


class Process(collections.Hashable):
    """
        Class for executing a pipeline process

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
        profile : str
            The execution environment for the process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : Command
            The `Command` instance that will be executing for running the process
        env : Optional[pathlib.Path]
            The location of the virtual environment
    """

    _cmd: Optional[Command] = None
    env: Optional[pathlib.Path] = None

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
        return f'<Process name={self.name} cmd="{self.cmd}">'

    def __str__(self) -> str:
        return self.name

    # TODO: Add profile and resource configuration setup also
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
            self.params.output_location = pathlib.Path(output_dir)
        self.update_location(str(self._output_location), category="output")
        if not self._output_location.is_absolute():
            raise FileNotFoundError(
                f"{self._output_location} must be an absolute path and must exist"
            )
        self._output_location.mkdir(exist_ok=True, parents=True)
        script = self.script.render()
        script_file = self._output_location / f"{self.name}.nf"
        LOG.logger.success(f"Building script: {script_file}")
        with open(script_file, "w") as fid:
            fid.write(script)
        config = self.config.render(self.params.dict, resource_config=True)
        config_file = self._output_location / f"{self.name}.config"
        LOG.logger.success(f"Building config: {config_file}")
        with open(config_file, "w") as fid:
            fid.write(config)
        work_dir = self._output_location / "work"
        if work_dir.exists():
            warning_msg = "Work directory already exists (could be from another run)"
            LOG.logger.warning(warning_msg)
            warn(warning_msg)
        else:
            work_dir.mkdir()

    # TODO: Also add profile and resource configuration scripts to `cmd` and `build`
    @property
    def cmd(self) -> Command:
        """
            The `Command` instance that will be used for executing the proces

            Returns
            -------
            Command
                The `Command` instance for the process
        """
        script_path = self._output_location / f"{self.name}.nf"
        config_path = self._output_location / f"{self.name}.config"
        work_dir = self._output_location / "work"
        if (
            not script_path.exists()
            or not config_path.exists()
            or not work_dir.exists()
        ):
            warning_msg = (
                "The process has not been built yet. Please run `build` before `run`"
            )
            LOG.logger.warning(warning_msg)
            warn(warning_msg)
        cmd = f"nextflow -C {config_path} run {script_path} -w {work_dir} -profile {self.profile}"
        if not self._cmd:
            self._cmd = Command(cmd, self.profile)
        else:
            self._cmd.update(cmd)
        return self._cmd

    def run(self) -> Command:
        """
            Starts the execution of the process and returns the Command instance
            This could produce unexpected results if run before `build`

            Returns
            -------
            Command
                The command object
                It has `cmd`, `out`, `pid` and other facilities
        """
        # TODO: This step also needs to fill in the profiles and resources templates
        self.cmd.run()
        return self.cmd

    def log(self) -> None:
        """ Logs the stdout and stderr of the process to the log_file """
        LOG.logger.info(
            f"Running process: {self.name} with profile {self.profile} and env {self.env}"
        )
        self.cmd.log()

    def wait(self) -> None:
        """ Wait for the process to complete or terminate """
        return self.cmd.wait()

    @property
    def output(self) -> str:
        """ Returns the output generated during execution of the process """
        return self.cmd.output

    @property
    def error(self) -> str:
        """ Returns the error generated during execution of the command """
        return self.cmd.error

    def clean(self, scope: str) -> None:
        """
            Cleans out the requested scope

            Parameters
            ----------
            scope : {'all', 'work_dir'}
                The scope to be cleaned
        """
        warning_msg = (
            "You are about to delete files and folders which is in irreversible process"
        )
        LOG.logger.warning(warning_msg)
        warn(warning_msg)
        if (
            not self._output_location.is_absolute()
            or not self._output_location.exists()
        ):
            raise FileNotFoundError(
                f"{self._output_location} does not exist or is not an absolute path"
            )
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
            raise ValueError(
                "Unsupported scope. Please choose from {'all', 'work_dir'}"
            )

    def attach_to(self, previous: "Process") -> None:
        """
            Update inputs of current `Process` instance using outputs of previous

            Parameters
            ----------
            previous : Process
                The `Process` instance to attach the current instance to
        """
        LOG.logger.info(f"Attaching IO of {previous.name} to {self.name}")
        self.params.attach_to(previous.params)

    def update_location(self, location: str, category: str) -> None:
        """
            Update the location of all Input and Output elements
            Useful for an intermediate process

            Parameters
            ----------
            location : str
                The location of the IO element
            category : {'input', 'output'}
                Specifies whether the data is input or output information
        """
        path = pathlib.Path(location)
        if not path.is_absolute():
            if str(path).startswith("~/"):
                str_path = str(path).replace("~/", str(path.home()))
                path = pathlib.Path(str_path)
            else:
                raise ValueError("location must be an absolute path")
        LOG.logger.info(
            f"Updating location of {category}s of {self.name} to {location}"
        )
        if category == "input":
            for input_ in self.params.input:
                in_location = input_.location
                if in_location is None:
                    continue
                if not in_location.is_absolute():
                    self.params.update_location(
                        input_.datatype, str(path / in_location), "input"
                    )
        if category == "output":
            for output_ in self.params.output:
                out_location = output_.location
                if out_location is None:
                    continue
                if not out_location.is_absolute():
                    self.params.update_location(
                        output_.datatype, str(path / out_location), "output"
                    )

    @property
    def status(self) -> str:
        """
            Return the status of the current process

            Returns
            -------
            str
                One of {'success', 'failure', 'in progress', 'not started'}
        """
        if self.cmd.status == "success":
            for output in self.params.output:
                if "*" in str(output.location):
                    str_loc = str(output.location)
                    ind = str_loc.find("*")
                    files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                    if files:
                        return "success"
                elif output.location.exists():
                    return "success"
            return "failure"
        else:
            return self.cmd.status


class InternalProcess(Process):
    """
        Class for executing an internal pipeline process

        Parameters
        ----------
        params : Params
            The parameters for the internal process
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
        profile : str
            The execution environment for the process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
    """

    def __init__(
        self,
        params: Params,
        profile: str,
        script_name: str = "process.nf",
        config_name: str = "process.config",
        process_dir_name: str = "processes",
    ) -> None:
        super().__init__(params, profile, script_name, config_name, process_dir_name)

    def __repr__(self) -> str:
        return f"<InternalProcess name={self.name} cmd={self.cmd}>"


class ExternalProcess(Process):
    """
        Class for executing an external pipeline process

        Parameters
        ----------
        params : Params
            The parameters for the external process
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
        profile : str
            The execution environment for the process
        script : ScriptTemplate
            The process script template
        config : ConfigTemplate
            The process configuration template
        cmd : str
            The command that will be executing for running the process
        env : pathlib.Path
            The location of the virtual environment
    """

    def __init__(
        self,
        params: Params,
        profile: str,
        script_name: str = "process.nf",
        config_name: str = "process.config",
        process_dir_name: str = "processes",
    ) -> None:
        super().__init__(params, profile, script_name, config_name, process_dir_name)
        self.env = self.params.env

    def __repr__(self) -> str:
        return f"<ExternalProcess name={self.name} cmd={self.cmd}>"
