"""
    Module to extract, process and store pipeline settings
"""

import pathlib

import toml

from .datatypes import DataTypes
from .params import ParamsSet


CONFIG_FOLDER = pathlib.Path(__file__).parent / "configs"


class Config:
    """
        Class to extract, process and store pipeline settings

        Parameters
        ----------
        config_folder : pathlib.Path
            The path to the folder containing the configuration files

        Attributes
        ----------
        datatypes : DataTypes
            The set of supported datatypes
        params_set : ParamsSet
            The dictionary containing process configurations
    """

    def __init__(self, config_folder: pathlib.Path = CONFIG_FOLDER) -> None:
        datatypes_file = config_folder / "datatypes.toml"
        with open(datatypes_file, "r") as fid:
            datatypes = DataTypes(toml.load(fid))
        self.datatypes = datatypes
        process_types = [
            "otu_assignment",
            "tax_assignment",
            "otu_processing",
            "network_inference",
        ]
        combined_params: dict = {}
        for process_type in process_types:
            fname = config_folder / f"{process_type}.toml"
            with open(fname, "r") as fid:
                params = toml.load(fid)
            for key, value in params.items():
                combined_params[key] = value
        params_set = ParamsSet(combined_params)
        self._check_io_integrity(params_set)
        self.params_set = params_set

    def _check_io_integrity(self, params_set: ParamsSet) -> None:
        """
            Verify whether all the datatypes in the params_set are valid

            Parameters
            ----------
            params_set : ParamsSet
                The params to be verified
        """
        for param in params_set:
            for curr_input in param.input:
                if curr_input.datatype not in self.datatypes:
                    raise ValueError(
                        f"Invalid datatype {curr_input.datatype} in input definition"
                    )
                formats = self.datatypes[curr_input.datatype].format
                for curr_format in curr_input.format:
                    if curr_format not in formats:
                        raise ValueError(
                            f"Unsupported format {curr_format} in input definition"
                        )
            for curr_output in param.output:
                if curr_output.datatype not in self.datatypes:
                    raise ValueError(
                        f"Invalid datatype {curr_output.datatype} in output definition"
                    )
                formats = self.datatypes[curr_output.datatype].format
                for curr_format in curr_output.format:
                    if curr_format not in formats:
                        raise ValueError(
                            f"Unsupported format {curr_format} in output definition"
                        )
                if not curr_output.location:
                    raise ValueError(
                        f"Relative location for output {curr_output} must be defined"
                    )
