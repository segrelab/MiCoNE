"""
    Module that defines the initialization for micone
"""

import pathlib
from typing import Iterable

from ..pipelines import Command
from ..logging import LOG


PIPELINE_DIR = pathlib.Path(__file__).parent.parent / "pipelines"


class Initialize:
    """A class that initializes the nextflow pipeline for a micone workflow"""

    def __init__(self) -> None:
        self.workflows_dir = PIPELINE_DIR / "workflows"
        self.templates_dir = PIPELINE_DIR / "templates"
        self.modules_dir = PIPELINE_DIR / "modules"
        self.functions_dir = PIPELINE_DIR / "functions"
        self.configs_dir = PIPELINE_DIR / "configs"
        self.data_dir = PIPELINE_DIR / "data"
        self.workflows = [w.stem for w in self.workflows_dir.iterdir()]

    def init(self, workflow: str, output_path: pathlib.Path) -> Iterable[Command]:
        """
        Initialize the requested workflow

        Parameters
        ----------
        workflow: str
            The workflow template to be used for initialization
        output_path : pathlib.Path
            The location where the pipeline template is to be created

        Yields
        ------
        Command
            The currently running initialization command
        """
        if workflow in self.workflows:
            LOG.logger.info(f"Initializing {workflow} workflow")
            nf_micone = output_path / "nf_micone"
            # mkdir -p nf_micone
            cmd1 = Command(f"mkdir -p {nf_micone}", profile="local")
            cmd1.run()
            yield cmd1
            # cp -r "${BASE_DIR}/templates" .
            cmd2 = Command(f"cp -r {self.templates_dir} {output_path}", profile="local")
            cmd2.run()
            yield cmd2
            # cp -r "${BASE_DIR}/modules" nf_micone
            cmd3 = Command(f"cp -r {self.modules_dir} {nf_micone}", profile="local")
            cmd3.run()
            yield cmd3
            # cp -r "${BASE_DIR}/functions" nf_micone
            cmd4 = Command(f"cp -r {self.functions_dir} {nf_micone}", profile="local")
            cmd4.run()
            yield cmd4
            # cp -r "${BASE_DIR}/configs" nf_micone
            cmd5 = Command(f"cp -r {self.configs_dir} {nf_micone}", profile="local")
            cmd5.run()
            yield cmd5
            # cp -r "${BASE_DIR}/data" nf_micone
            cmd6 = Command(f"cp -r {self.data_dir} {nf_micone}", profile="local")
            cmd6.run()
            yield cmd6
            # copy main.nf, nextflow.config, samplesheet.csv, metadata.json, run.sh
            workflow_dir = self.workflows_dir / workflow
            cmd7 = Command(
                f"cp {workflow_dir}/main.nf {workflow_dir}/nextflow.config {workflow_dir}/samplesheet.csv {workflow_dir}/metadata.json {workflow_dir}/run.sh {output_path}",
                profile="local",
            )
            cmd7.run()
            yield cmd7
        else:
            raise ValueError(
                f"{workflow} not a supported workflow. Use one of {self.workflows}"
            )
