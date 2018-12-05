"""
    Module that defines the environment setup for external processes
"""

import pathlib
from typing import Optional, List

from ..pipelines import Command


EX_PIPELINE_DIR = pathlib.Path(__file__).parent.parent / "pipelines/src/external"


class Environments:
    """
        A class that creates, lists and loads conda environments

        Parameters
        ----------

        Attributes
        ----------
        configs : List[pathlib.Path]
            The list of locations of the environment config files
        env_locs : List[pathlib.Path]
            The list of locations of environments
        env_names : List[str]
            The list of names of environments
    """

    def __init__(self) -> None:
        self.configs = list(EX_PIPELINE_DIR.glob("**/env.yml"))
        self.env_locs = [c.parent / "env" for c in self.configs]
        self.env_names = [str(c.parent) for c in self.configs]

    def init(self, env: Optional[str] = None) -> None:
        """
            Initialize the requested conda environment

            Parameters
            ----------
            env : Optional[str]
                The name of the conda environment to initialize
                If None then all the listed conda environments will be initialized
                Default value is None
        """
        if env is None:
            for config, env_loc in zip(self.configs, self.env_locs):
                cmd = f"conda create -f {config} -p {env_loc}"
                init_cmd = Command(cmd, profile="local")
                init_cmd.run()
        if env in self.env_names:
            ind = self.env_names.index(env)
            config = self.configs[ind]
            env_loc = self.env_locs[ind]
            cmd = f"conda create -f {config} -p {env_loc}"
            init_cmd = Command(cmd, profile="local")
            init_cmd.run()
        if env not in self.env_names:
            raise ValueError(f"{env} not a supported environment")

    def load(self, env: str) -> None:
        """
            Load the requested conda environment

            Parameters
            ----------
            env : str
                The name of the conda environment to load

        """
        if env not in self.env_names:
            raise ValueError(f"{env} not a supported environment")
        ind = self.env_names.index(env)
        env_loc = self.env_locs[ind]
        cmd = f"source activate {env_loc}"
        load_cmd = Command(cmd, profile="local")
        load_cmd.run()
