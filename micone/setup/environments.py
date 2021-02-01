"""
    Module that defines the environment setup for processes
"""

import pathlib
from typing import Iterable, Optional

from ..pipelines import Command
from ..logging import LOG


ENV_DIR = pathlib.Path(__file__).parent.parent / "pipelines/envs"


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
        self.configs = list(ENV_DIR.glob("**/env.yml"))
        self.env_names = [f"{c.parent.stem}" for c in self.configs]

    def init(self, env: Optional[str] = None) -> Iterable[Command]:
        """
        Initialize the requested conda environment

        Parameters
        ----------
        env : Optional[str]
            The name of the conda environment to initialize
            If None then all the listed conda environments will be initialized
            Default value is None

        Yields
        ------
        Command
            The currently running initialization command
        """
        if env is None:
            for config, env_name in zip(self.configs, self.env_names):
                LOG.logger.info(f"Initializing {env_name} environment")
                cmd_str = f"conda env create -f {config} -n {env_name}"
                init_cmd = Command(cmd_str, profile="local", timeout=10000)
                init_cmd.run()
                yield init_cmd
        elif env in self.env_names:
            ind = self.env_names.index(env)
            config = self.configs[ind]
            env_name = self.env_names[ind]
            LOG.logger.info(f"Initializing {env_name} environment")
            cmd_str = f"conda env create -f {config} -n {env_name}"
            init_cmd = Command(cmd_str, profile="local", timeout=10000)
            init_cmd.run()
            yield init_cmd
        elif env not in self.env_names:
            raise ValueError(f"{env} not a supported environment")

    def post_install(self, env: Optional[str] = None) -> Iterable[Command]:
        """
        Run any post installation scripts for environment setup

        Parameters
        ----------
        env : Optional[str]
            The name of the conda environment to setup
            If None then all the listed conda environments will be initialized
            Default value is None

        Yields
        ------
        Command
            The currently running post_install command
        """
        if env is None:
            post_scripts = list(ENV_DIR.glob("**/post_install.sh"))
        else:
            post_scripts = list(ENV_DIR.glob(f"**/{env}/post_install.sh"))
        for script in post_scripts:
            cmd_str = f"bash {script}"
            LOG.logger.info(f"Running post_install for {env} environment")
            post_cmd = Command(cmd_str, profile="local", timeout=10000)
            post_cmd.run()
            yield post_cmd

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
        cmd_str = f"source activate {env_name}"
        LOG.logger.info(f"Loading {env} environment")
        load_cmd = Command(cmd_str, profile="local", timeout=10000)
        load_cmd.run()
