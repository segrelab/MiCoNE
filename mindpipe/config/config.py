"""
    Module to extract, process and store pipeline settings
"""

import pathlib
from typing import Union

import toml

from .datatypes import DataTypes
from .params import InternalParamsSet, ExternalParamsSet


CONFIG_FOLDER = pathlib.Path(__file__).parent
DATATYPES_FILE = CONFIG_FOLDER / "datatypes.toml"
EXTERNAL_FILE = CONFIG_FOLDER / "external.toml"
INTERNAL_FILE = CONFIG_FOLDER / "internal.toml"
ParamType = Union[InternalParamsSet, ExternalParamsSet]


class Config:
    """
        Class to extract, process and store pipeline settings

        Parameters
        ----------
        datatypes_file : pathlib.Path
            The path to the datatypes definition file
        external_file : pathlib.Path
            The path to the external process defintion file
        internal_file : pathlib.Path
            The path to the internal process defintion file

        Attributes
        ----------
        datatypes : DataTypes
            The set of supported datatypes
        process_params : Dict[str, ParamType]
            The dictionary containing internal and external process configurations
    """

    def __init__(
            self,
            datatypes_file: pathlib.Path = DATATYPES_FILE,
            external_file: pathlib.Path = EXTERNAL_FILE,
            internal_file: pathlib.Path = INTERNAL_FILE,
    ) -> None:
        with open(datatypes_file, 'r') as fid:
            datatypes = DataTypes(toml.load(fid))
        self.datatypes = datatypes
        with open(external_file, 'r') as fid:
            external_params = ExternalParamsSet(toml.load(fid))
        self._check_io_integrity(external_params)
        with open(internal_file, 'r') as fid:
            internal_params = InternalParamsSet(toml.load(fid))
        self._check_io_integrity(internal_params)
        self.process_params = {
            "internal": internal_params,
            "external": external_params,
        }

    def _check_io_integrity(self, process_params: ParamType) -> None:
        """
            Verify whether all the datatypes in the process_params are valid

            Parameters
            ----------
            process_params : ParamType
                The params to be verified
        """
        for param in process_params:
            for curr_input in param.input:
                if curr_input.datatype not in self.datatypes:
                    raise ValueError(f"Invalid datatype {curr_input.datatype} in input definition")
                formats = self.datatypes[curr_input.datatype].format
                for curr_format in curr_input.format:
                    if curr_format not in formats:
                        raise ValueError(f"Unsupported format {curr_format} in input definition")
            for curr_output in param.output:
                if curr_output.datatype not in self.datatypes:
                    raise ValueError(f"Invalid datatype {curr_output.datatype} in output definition")
                formats = self.datatypes[curr_output.datatype].format
                for curr_format in curr_output.format:
                    if curr_format not in formats:
                        raise ValueError(f"Unsupported format {curr_format} in output definition")
                if not curr_output.location:
                    raise ValueError(f"Relative location for output {curr_output} must be defined")
