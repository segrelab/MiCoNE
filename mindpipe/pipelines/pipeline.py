"""
    Module that defines a complete pipeline by incorporating settings and processes
"""

import collections
from typing import Iterator, List, Union

import toml

from ..config import Config
from .process import InternalProcess, ExternalProcess


class Pipeline(collections.Sequence):
    """
        Class that defines the pipeline and contains methods to run the pipeline

        Parameters
        ----------
        user_settings_file : str
            The user created settings file that describes the pipeline
        profile : {'local', 'sge'}
            The execution environment

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
        processes : List[Union[InternalProcess, ExternalProcess]]
            The list of `Process` in the pipeline
    """

    _req_keys = {"title", "order", "output_location"}

    def __init__(self, user_settings_file: str, profile: str, **kwargs) -> None:
        self.config = Config()
        self.profile = profile
        user_settings = self._parse_settings(user_settings_file, **kwargs)
        title = kwargs.get("title")
        order = kwargs.get("order")
        output_location = kwargs.get("output_location")
        self._order = order if order else user_settings["order"]
        self.title = title if title else user_settings["title"]
        self.output_location = (
            output_location if output_location else user_settings["output_location"]
        )
        self.processes = self._create_processes(user_settings)

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
            if key not in settings or key not in kwargs:
                raise ValueError(
                    f"Required key {key} not in user_settings or parameters"
                )
        return settings

    def _create_processes(self, settings):
        process_list: List[Union[InternalProcess, ExternalProcess]] = []
        process_namelist = self._order
        for process_name in process_namelist:
            if "." in process_name:
                temp = settings
                for x in process_name.split("."):
                    temp = temp[x]
                user_process_data = temp
            else:
                user_process_data = settings[process_name]
            process_data = self.config.process_params[user_process_data["module"]][
                process_name
            ]
            process_data.merge(user_process_data)
            if user_process_data["module"] == "internal":
                process_list.append(InternalProcess(process_data, self.profile))
            elif process_data["module"] == "external":
                process_list.append(ExternalProcess(process_data, self.profile))
            else:
                raise ValueError(f"Unsupported process type: {process_data['module']}")
        for i, current_process in enumerate(process_list[1:]):
            for previous_process in reversed(process_list[:i]):
                current_process.attach_to(previous_process)
            current_process.update_location(self.output_location)
        return process_list

    def __iter__(self) -> Iterator:
        return iter(self.processes)

    def __len__(self) -> int:
        return len(self.processes)

    def __getitem__(self, key: str) -> Union[InternalProcess, ExternalProcess]:
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

    # TODO: Create a run method
