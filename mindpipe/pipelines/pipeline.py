"""
    Module that defines a complete pipeline by incorporating settings and processes
"""

import collections
import pathlib
from typing import Iterator, List, Optional

import networkx as nx
import toml

from ..config import Config
from .process import Process


class Pipeline(collections.Sequence):
    """
        Class that defines the pipeline and contains methods to run the pipeline

        Parameters
        ----------
        user_settings_file : str
            The user created settings file that describes the pipeline
        profile : {'local', 'sge'}
            The execution environment
        base_dir : str, optional
            The absolute location of the base directory for the input files
            This needs to be supplied if the input files location in the settings are relative
            If None, then current working directory is used
        resume : bool, optional
            The flag to determine whether a previous execution is resumed
            Default value is False

        Other Parameters
        ----------------
        title : str, optional
            The title of the pipeline
        order : List[str], optional
            The order of the processes in the pipeline
        output_location : str, optional
            The base output location to store all pipeline results

        Attributes
        ----------
        title : str
            The title of the pipeline
        output_location : str
            The base output location to store all pipeline results
        config : Config
            The configuration object for the `mindpipe` pipelines
        profile : str
            The execution environment for the pipeline
        base_dir : pathlib.Path
            The absolute path to the base input file directory
        processes : List[Process]
            The list of `Process` in the pipeline
    """

    _req_keys = {"title", "order", "output_location"}

    def __init__(
        self,
        user_settings_file: str,
        profile: str,
        base_dir: Optional[str] = None,
        resume: Optional[bool] = False,
        **kwargs,
    ) -> None:
        self.config = Config()
        self.profile = profile
        self.resume = resume
        if base_dir is None:
            self.base_dir = pathlib.Path.cwd()
        else:
            base_path = pathlib.Path(base_dir)
            if base_path.is_absolute() and base_path.exists():
                self.base_dir = base_path
            else:
                raise ValueError("base_dir path must be absolute and must exist")
        user_settings = self._parse_settings(user_settings_file, **kwargs)
        title = kwargs.get("title")
        order = kwargs.get("order")
        output_location = kwargs.get("output_location")
        self._process_tree = self._parse_process_tree(
            order if order else user_settings["order"]
        )
        self.title = title if title else user_settings["title"]
        self.output_location = (
            output_location if output_location else user_settings["output_location"]
        )
        self.processes = self._create_processes(user_settings)

    @staticmethod
    def _parse_process_tree(process_string: str) -> nx.Graph:
        """
            Parses the process string and creates a process tree from it

            Parameters
            ----------
            process_string : str
                The string that represents the process tree

            Returns
            -------
            nx.Graph
                A nx.Graph representing the process tree
        """
        processes = [
            p for p in process_string.strip().replace("\n", " ").split(" ") if p
        ]
        graph = nx.DiGraph()
        process_stack = [processes[0]]
        delimiters = {"(", ")", "|"}
        for process in processes[1:]:
            print(process)
            if process not in delimiters:
                parent = process_stack.pop()
                graph.add_edge(parent, process)
                print(parent, process)
                process_stack.append(process)
            elif process == "(":
                process_stack.append(process_stack[-1])
            elif process == "|":
                process_stack.pop()
                process_stack.append(process_stack[-1])
            elif process == ")":
                process_stack.pop()
        return graph

    def _parse_settings(self, settings_file: str, **kwargs) -> dict:
        """
            Parses the user created settings file

            Parameters
            ----------
            settings_file : str
                The user defined settings file that describes the pipeline

            Returns
            -------
            dict
                The dictionary of verified user settings
        """
        with open(settings_file, "r") as fid:
            settings = toml.load(fid)
        for key in self._req_keys:
            if key not in settings and key not in kwargs:
                raise ValueError(
                    f"Required key '{key}' not found in user_settings or parameters to constructor"
                )
        return settings

    def _create_processes(self, settings):
        process_list: List[Process] = []
        process_namelist = self._process_tree
        for process_name in process_namelist:
            level_1, level_2, level_3 = process_name.split(".")
            user_process_data = settings[level_1][level_2][level_3]
            process_data = self.config.params_set[process_name]
            process_data.merge(user_process_data)
            process_list.append(Process(process_data, self.profile, resume=self.resume))
        process_list[0].update_location(str(self.base_dir), "input")
        process_list[0].update_location(self.output_location, "output")
        for i, current_process in enumerate(process_list[1:]):
            current_process.update_location(str(self.base_dir), "input")
            for previous_process in reversed(process_list[: i + 1]):
                current_process.attach_to(previous_process)
            current_process.update_location(self.output_location, "output")
        return process_list

    def __iter__(self) -> Iterator:
        return iter(self.processes)

    def __len__(self) -> int:
        return len(self.processes)

    def __getitem__(self, key: str) -> Process:
        for process in self:
            if process.name == key:
                return process
        raise KeyError(f"{key} is not a process of this pipeline")

    def __repr__(self) -> str:
        processes = [process.name for process in self]
        return (
            f"<Pipeline title={self.title} output_location={self.output_location} "
            f"processes={processes}>"
        )

    def __str__(self) -> str:
        return self.title

    def run(self) -> Iterator[Process]:
        """
            Starts the execution of the pipeline
            Returns an iterator over the processes being executed

            Returns
            -------
            Iterator[Process]
                Iterator over each process currently being executed
       """
        for process in self.processes:
            loc = pathlib.Path(self.output_location)  # / process.params.output_location
            if self.resume and process.io_exist:
                yield process
            else:
                process.build(str(loc))
                process.run()
                yield process

    # TODO: Create computational metadata
