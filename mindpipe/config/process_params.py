"""
    Module to parse and store pipeline settings
"""

import collections
import pathlib
from typing import Any, Dict, Iterator, List, Set, Tuple, Union


PIPELINE_DIR = pathlib.Path.cwd().parent / "pipelines"
Input = collections.namedtuple("Input", ['datatype', 'format'])
Output = collections.namedtuple("Output", ['datatype', 'format', 'location'])
IOType = Union[Input, Output]


class ProcessParams(collections.Hashable):
    """
        The class for parsing and storing the parameters of a process

        Parameters
        ----------
        data : Dict[str, Any]
            The information about the parameters for a particular process

        Attributes
        ----------
        name : str
            Process name
        root : pathlib.Path
            Root directory where the process pipeline is stored
        env : pathlib.Path
            Location of the virtual environment for the process
        output_location : pathlib.Path
            Directory relative to main output directory where results of the process are to be saved
        input : Set[Input]
            The list of inputs of the process
        output : Set[Output]
            The list of outputs of the process
        parameters : Set[Dict[str, Any]]
            The list of parameters of the process
    """
    _req_keys = {
        "root",
        "output_location",
        "input",
        "output",
        "parameters"
    }

    def __init__(self, data: Tuple[str, Dict[str, Any]]) -> None:
        if len(data) != 2:
            raise ValueError(f"Invalid process data: {data}")
        key, value = data
        for req_key in self._req_keys:
            if req_key not in value:
                raise ValueError(f"Invalid process data. {req_key} not found")
        self.name = key
        self.root = PIPELINE_DIR / value["root"]
        if not self.root.exists() or not self.root.is_dir():
            raise FileNotFoundError(
                f"The root directory: {self.root} doesn't exist. "
                "Please reinstall the package"
            )
        if "env" in value:
            self.env = PIPELINE_DIR / value["env"]
        else:
            self.env = None
        if not self.env.exists() or not self.env.is_dir():
            raise FileNotFoundError(
                f"The directory for the environment: {self.env} doesn't exist. "
                "Please reinstall the package"
            )
        self.output_location = pathlib.Path(value["output_location"])
        self.input = self._process_io(value["input"], "input")
        self.output = self._process_io(value["output"], "output")
        self.parameters = value["parameters"]

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        inputs = {i.datatype for i in self.input}
        outputs = {o.datatype for o in self.output}
        return f"<ProcessParams name={self.name} input={inputs} output={outputs}>"

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def _process_io(data: List[Dict[str, Union[str, List[str]]]], category: str) -> Set[IOType]:
        """
            Process the input information

            Parameters
            ----------
            data : List[Dict[str, Union[str, List[str]]]]
                The input/output information
            category: {'input', 'output'}
                Specifies whether the data is input or output information

            Returns
            -------
            List[IOType]
                Processed input/output information
        """
        if category == "input":
            IO = Input
        elif category == "output":
            IO = Output
        else:
            raise TypeError("Category can only be either 'Input' or 'Output'")
        inputs: Set[IOType] = set()
        for item in data:
            for field in IO._fields:
                if field not in item:
                    raise ValueError(f"Invalid input: {data}. Missing {field}")
            for field in item:
                if field not in IO._fields:
                    raise ValueError(f"Invalid input: {data}. Extra {field}")
            inputs.add(IO(**item))
        return inputs


class ProcessParamsSet(collections.Set):
    """
        The set of all supported pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self.processes: Set[ProcessParams] = set()
        for key, value in data.items():
            process_params = ProcessParams((key, value))
            if process_params in self.processes:
                raise ValueError("Duplicate process definitions detected in settings. Aborting")
            self.processes.add(process_params)

    def __iter__(self) -> Iterator:
        return iter(self.processes)

    def __len__(self) -> int:
        return len(self.processes)

    def __contains__(self, value: str) -> bool:
        return value in [process.name for process in self.processes]

    def __getitem__(self, key: str) -> ProcessParams:
        for process in self.processes:
            if process.name == key:
                return process
        raise KeyError(f"{key} is not in ProcessParamsSet")

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<ProcessParamsSet n={len(self)} processes={processes}>"


class InternalProcessParamsSet(ProcessParamsSet):
    """
        The set of all supported internal pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the internal pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<InternalProcessParamsSet n={len(self)} processes={processes}>"


class ExternalProcessParamsSet(ProcessParamsSet):
    """
        The set of all supported external pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the external pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        data_processed = {}
        for level_1 in data:
            for level_2 in level_1:
                for level_3 in level_2:
                    name = f"{level_1}.{level_2}.{level_3}"
                    data_processed[name] = data[level_1][level_2][level_3]
        super().__init__(data_processed)

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<ExternalProcessParamsSet n={len(self)} processes={processes}>"
