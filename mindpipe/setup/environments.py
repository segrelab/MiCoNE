"""
    Module that defines the environment setup for external processes
"""

import pathlib
from typing import Iterable, Optional

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
        env_names : List[str]
            The list of names of environments
    """

    def __init__(self) -> None:
        self.configs = list(EX_PIPELINE_DIR.glob("**/env.yml"))
        self.env_names = [f"mindpipe-{c.parent.stem}" for c in self.configs]

    def init(self, env: Optional[str] = None) -> Iterable[Command]:
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
            for config, env_name in zip(self.configs, self.env_names):
                cmd = f"conda env create -f {config} -n {env_name}"
                init_cmd = Command(cmd, profile="local")
                init_cmd.run()
                yield init_cmd
        elif env in self.env_names:
            ind = self.env_names.index(env)
            config = self.configs[ind]
            env_name = self.env_names[ind]
            cmd = f"conda env create -f {config} -n {env_name}"
            init_cmd = Command(cmd, profile="local")
            init_cmd.run()
            yield init_cmd
        elif env not in self.env_names:
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
        env_name = self.env_names[ind]
        cmd = f"source activate {env_name}"
        load_cmd = Command(cmd, profile="local")
        load_cmd.run()
