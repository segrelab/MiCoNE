"""
    Module that defines different pipeline processes
"""

import collections
from copy import deepcopy
import pathlib
import re
import shutil
from typing import Any, Dict, Optional
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
    output_location : str
        The absolute path to the base input file directory
    id_ : str, optional
        The unique id_ given to the process in the process tree
        Default value is None, in this case process name is used as id_
    root_dir : str, optional
        The root directory for the results of the current process
        Default value is None
    script_name : str, optional
        The name of the process script template
        Default is 'process.nf'
    config_name : str, optional
        The name of the process configuration template
        Default is 'process.config'
    process_dir_name : str, optional
        The name of the process directory where the templates are stored
        Default is 'processes'
    project : str, optional
        The project under which to run the pipeline on the 'sge'
        Default value is None
    resume: bool, optional
        The flag to determine whether a previous execution is resumed
        Default value is False

    Attributes
    ----------
    id_ : str
        The unique id_ given to the process in the process tree
    name : str
        The name of the process
    params : Params
        The core parameters object for the process
    profile : str
        The execution environment for the process
    project : str
        The project under which to run the pipeline on the 'sge'
    script : ScriptTemplate
        The process script template
    config : ConfigTemplate
        The process configuration template
    cmd : Command
        The `Command` instance that will be executing for running the process
    env : pathlib.Path
        The location of the virtual environment
    """

    _cmd: Optional[Command] = None

    def __init__(
        self,
        params: Params,
        profile: str,
        output_location: str,
        id_: Optional[str] = None,
        root_dir: Optional[str] = None,
        script_name: str = "process.nf",
        config_name: str = "process.config",
        process_dir_name: str = "processes",
        project: Optional[str] = None,
        resume: Optional[bool] = False,
    ) -> None:
        self.params = deepcopy(params)
        self.name = self.params.name
        self.profile = profile
        self.project = project
        self.resume = resume
        self.id_ = id_ if id_ else self.name
        self.output_location = pathlib.Path(output_location)
        script_file = self.params.root / script_name
        process_dir = self.params.root / process_dir_name
        config_file = self.params.root / config_name
        self.script = ScriptTemplate(script_file, process_dir)
        self.config = ConfigTemplate(config_file)
        if root_dir:
            self.params.root_dir = pathlib.Path(root_dir)
        self.env = self.params.env

    def __hash__(self) -> int:
        return hash(self.id_)

    def __repr__(self) -> str:
        return f'<Process name={self.id_} cmd="{self.cmd}">'

    def __str__(self) -> str:
        return self.id_

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
            self.output_location = pathlib.Path(output_dir)
        root_path = self.output_location / self.params.root_dir
        self.update_location(str(root_path), category="output")
        if not self.output_location.is_absolute():
            raise FileNotFoundError(f"{self.output_location} must be an absolute path")
        self.output_location.mkdir(exist_ok=True, parents=True)
        script = self.script.render()
        script_file = self.output_location / f"{self.id_}.nf"
        LOG.logger.success(f"Building script: {script_file}")
        with open(script_file, "w") as fid:
            fid.write(script)
        config = self.config.render(self.dict, resource_config=True)
        config_file = self.output_location / f"{self.id_}.config"
        LOG.logger.success(f"Building config: {config_file}")
        with open(config_file, "w") as fid:
            fid.write(config)
        work_dir = self.output_location / "work"
        if work_dir.exists():
            warning_msg = "Work directory already exists (could be from another run)"
            LOG.logger.warning(warning_msg)
        else:
            work_dir.mkdir()

    @property
    def cmd(self) -> Command:
        """
        The `Command` instance that will be used for executing the proces

        Returns
        -------
        Command
            The `Command` instance for the process
        """
        script_path = self.output_location / f"{self.id_}.nf"
        config_path = self.output_location / f"{self.id_}.config"
        log_path = self.output_location / f"{self.id_}.log"
        work_dir = self.output_location / "work"
        cmd = (
            f"nextflow -C {config_path} -log {log_path} run {script_path} -w {work_dir} "
            f"-profile {self.profile}"
        )
        # if self.resume:
        #     cmd += " -resume"
        if not self._cmd:
            self._cmd = Command(cmd, "local", timeout=100_000)
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
        script_path = self.output_location / f"{self.id_}.nf"
        config_path = self.output_location / f"{self.id_}.config"
        work_dir = self.output_location / "work"
        env = self.params.env
        if not env or not env.exists() or not env.is_dir():
            raise FileNotFoundError(
                f"The environment for the process: {self.name} doesn't exist. "
                f"Please run micone init --env {self.params.env_name}"
            )
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
        self.cmd.run()
        return self.cmd

    def log(self) -> None:
        """ Logs the stdout and stderr of the process to the log_file """
        LOG.logger.info(
            f"Running process: {self.id_} with profile {self.profile} and env {self.env}"
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
        if not self.output_location.is_absolute() or not self.output_location.exists():
            raise FileNotFoundError(
                f"{self.output_location} does not exist or is not an absolute path"
            )
        script_path = self.output_location / f"{self.id_}.nf"
        config_path = self.output_location / f"{self.id_}.config"
        log_path = self.output_location / f"{self.id_}.log"
        work_dir = self.output_location / "work"
        if scope == "all":
            shutil.rmtree(work_dir)
            script_path.unlink()
            config_path.unlink()
            log_path.unlink()
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
        LOG.logger.info(f"Attaching IO of {previous.name} to {self.id_}")
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
        LOG.logger.info(f"Updating location of {category}s of {self.id_} to {location}")
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
            One of {'success', 'resumed', 'failure', 'in progress', 'not started'}
        """
        if self.cmd.status == "success":
            output_status = self._check_files("output")
            if output_status:
                return "success"
            return "failure"
        if self.io_exist:
            return "resumed"
        return self.cmd.status

    def _check_files(self, category: str) -> bool:
        """
        Return True if files in the category are present o/w False

        Parameters
        ----------
        category: {'input', 'output'}
            Specifies whether the data is input or output information

        Returns
        -------
        bool
            True if the expected files exist
        """
        mult_pattern = re.compile(".*{(.*)}.*")
        if category == "input":
            io_object = self.params.input
        elif category == "output":
            io_object = self.params.output
        else:
            raise ValueError(
                f"Invalid category: {category}. Can either be 'input' or 'output'"
            )
        for io_item in io_object:
            loc = io_item.location
            if loc is None:
                return False
            if "*" in str(loc):
                str_loc = str(loc)
                mult_match = re.match(mult_pattern, str_loc)
                if mult_match:
                    str_loc_list = []
                    for pattern in mult_match.group(1).split(","):
                        str_loc_list.append(re.sub(r"{.*}", pattern, str_loc))
                else:
                    str_loc_list = [str_loc]
                for str_loc in str_loc_list:
                    ind = str_loc.find("*")
                    files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                    if len(files) == 0:
                        return False
            elif not loc.exists():
                return False
        return True

    @property
    def io_exist(self) -> bool:
        """
        Return True if the expected input and output of the process already exist
        Useful when resuming a pipeline execution

        Returns
        -------
        bool
            True if the expected input and output of the process already exist
        """
        input_exists = self._check_files("input")
        output_exists = self._check_files("output")
        return input_exists and output_exists

    def verify_io(self) -> None:
        """
        Verify whether the Input and Output elements have been assigned and are valid
        """
        mult_pattern = re.compile(".*{(.*)}.*")
        if not self.output_location.is_absolute():
            raise ValueError("The output location must be absolute")
        for elem in self.params.input:
            if elem.location is None:
                raise ValueError(
                    f"Input: {elem} has not been assigned a location yet for process.id_: {self.id_}"
                )
            if "*" in str(elem.location):
                str_loc = str(elem.location)
                mult_match = re.match(mult_pattern, str_loc)
                if mult_match:
                    str_loc_list = []
                    for pattern in mult_match.group(1).split(","):
                        str_loc_list.append(re.sub(r"{.*}", pattern, str_loc))
                else:
                    str_loc_list = [str_loc]
                for str_loc in str_loc_list:
                    ind = str_loc.find("*")
                    files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                    if len(files) == 0:
                        raise FileNotFoundError(
                            f"Unable to locate input files at {elem.location} for process.id_: {self.id_}"
                        )
            elif not elem.location.exists():
                raise FileNotFoundError(
                    f"Unable to locate input file at {elem.location} for process.id_: {self.id_}"
                )
        for elem in self.params.output:
            if elem.location is None:
                raise ValueError(
                    f"Output: {elem} has not been assigned a location yet for process.id_: {self.id_}"
                )
            if not elem.location.is_absolute():
                raise ValueError(
                    "Not all the output objects have absolute paths for process.id_: {self.id_}"
                )

    @property
    def dict(self) -> Dict[str, Any]:
        """
        Return data as a dictionary

        Returns
        -------
        Dict[str, Any]
            The data stored return as a dictionary
        """
        self.verify_io()
        data: Dict[str, Any] = dict()
        data["input"] = {
            elem.datatype: str(elem.location) for elem in self.params.input
        }
        data["output"] = {
            elem.datatype: str(elem.location) for elem in self.params.output
        }
        data["output_dir"] = self.output_location / self.params.root_dir
        data["env"] = self.env
        data["project"] = self.project
        for process_params in self.params.parameters:
            data[process_params.process] = process_params.params
        return data


def stringizer(process: Process) -> str:
    """
    Convert process to string for storage in GML file

    Parameters
    ----------
    process : Process
        The process instance to be converted to string

    Returns
    -------
    str
        Stringized process
    """
    return str(process)
