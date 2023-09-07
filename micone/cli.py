"""
    Console script for micone
"""

import pathlib
import pprint
import shutil
from typing import List

import click

from .logging import LOG
from .setup import Environments, Initialize
from .utils import Spinner
from .validation import check_results


@click.group()
@click.option(
    "--log", "-l", default=True, type=bool, help="Flag to turn on/off logging"
)
@click.option(
    "--interactive", "-i", default=True, type=bool, help="Flag to turn on/off spinner"
)
@click.pass_context
def cli(ctx, log: bool, interactive: bool):
    """Main entry point to micone"""
    spinner = Spinner(text="Starting up...", spinner="dots", interactive=interactive)
    spinner.start()
    ctx.obj["SPINNER"] = spinner
    spinner.succeed("Successfully initialized micone")
    if log:
        LOG.enable()
        click.secho(f"Log file is at {LOG.path}")


@cli.command()
@click.option(
    "--env",
    "-e",
    default=None,
    type=str,
    help="The environment to initialize. By default will initialize all",
)
@click.pass_context
def install(ctx, env: str):
    """Initialize the package and environments"""
    spinner = ctx.obj["SPINNER"]
    environments = Environments()
    for env_cmd in environments.init(env):
        spinner.start()
        spinner.text = f"Initializing environment: {env_cmd}"
        env_cmd.wait()
        env_cmd.log()
        if env_cmd.status == "failure":
            spinner.fail(f"{env_cmd} Failed")
        elif env_cmd.status == "success":
            spinner.succeed(f"{env_cmd} Passed")
    for post_cmd in environments.post_install(env):
        spinner.start()
        spinner.text = f"Running post installation: {post_cmd}"
        post_cmd.wait()
        post_cmd.log()
        if post_cmd.status == "failure":
            spinner.fail(f"{post_cmd} Failed")
        elif post_cmd.status == "success":
            spinner.succeed(f"{post_cmd} Passed")
    click.secho(f"Log file is at {LOG.path}")
    LOG.cleanup()


@cli.command()
@click.option(
    "--workflow",
    "-w",
    default="full",
    type=str,
    help="The micone workflow initialize: 'full', 'ta_op_ni', 'op_ni', or 'ni'",
)
@click.option(
    "--output_location",
    "-o",
    type=click.Path(exists=True),
    default=None,
    help="The output path to initialize workflow",
)
@click.pass_context
def init(
    ctx,
    workflow: str,
    output_location: click.Path,
):
    """Initialize the nextflow templates for the micone workflow"""
    spinner = ctx.obj["SPINNER"]
    initializer = Initialize()
    if not output_location:
        output_path = pathlib.Path()
    else:
        output_path = pathlib.Path(str(output_location))
    for init_cmd in initializer.init(workflow, output_path):
        spinner.start()
        spinner.text = f"Initializing the {workflow} workflow"
        init_cmd.wait()
        init_cmd.log()
        if init_cmd.status == "failure":
            spinner.fail(f"{init_cmd} Failed")
        elif init_cmd.status == "success":
            spinner.succeed(f"{init_cmd} Passed")
    click.secho(f"Log file is at {LOG.path}")
    LOG.cleanup()


@cli.command()
@click.option(
    "--workflow_dir",
    "-d",
    type=click.Path(exists=True),
    default=None,
    help="The workflow directory to be cleaned",
)
@click.option(
    "--clean_level",
    "-c",
    type=str,
    default="logs",
    help="Clean level can be logs, logs+work, logs+work+outputs, etc.",
)
@click.pass_context
def clean(ctx, workflow_dir: click.Path, clean_level: str):
    """Clean files from a pipeline run in the current directory.
    This command irrevesibly deletes content, use with caution
    """
    del_contents = clean_level.split("+")
    click.confirm(
        f"Are you sure you want to delete {del_contents} in current directory?",
        abort=True,
    )
    if workflow_dir is None:
        workflow_path = pathlib.Path()
    else:
        workflow_path = pathlib.Path(str(workflow_dir))
    spinner = ctx.obj["SPINNER"]
    spinner.start()
    spinner.text = "Cleaning up pipeline files"
    if "logs" in del_contents:
        spinner.text = "Deleting logs"
        # Delete nextflow log file
        for log_file in workflow_path.glob(".nextflow.*"):
            log_file.unlink()
        # Delete nextflow log folder
        shutil.rmtree(workflow_path / ".nextflow", ignore_errors=True)
        # Delete dag files
        for dag_file in workflow_path.glob("*.html.*"):
            dag_file.unlink()
        # Delete trace files
        for trace_file in workflow_path.glob("*.txt.*"):
            trace_file.unlink()
        spinner.succeed("Completed deletion of logs, old traces and dags")
    if "work" in del_contents:
        spinner.text = "Deleting work"
        # Delete work directory
        shutil.rmtree(workflow_path / "work", ignore_errors=True)
        spinner.succeed("Completed deletion of work")
    if "outputs" in del_contents:
        spinner.text = "Deleting outputs"
        # Delete outputs directory
        shutil.rmtree(workflow_path / "outputs", ignore_errors=True)
        spinner.succeed("Completed deletion of outputs")
    spinner.succeed("Completed cleanup")


@cli.command()
@click.option(
    "--workflow_dir",
    "-d",
    type=click.Path(exists=True),
    help="The pipeline execution directory",
)
@click.option(
    "--procs",
    "-p",
    type=click.INT,
    default=4,
    help="Number of processors to use",
)
@click.pass_context
def validate_results(ctx, workflow_dir: click.Path, procs: int):
    """Check results of the pipeline execution"""
    pipeline_dir = pathlib.Path(str(workflow_dir))
    spinner = ctx.obj["SPINNER"]
    spinner.start()
    spinner.text = "Checking pipeline execution"
    (
        pipeline_results,
        trace_results,
        biom_results,
        network_results,
        output_results,
    ) = check_results(pipeline_dir, procs)
    if pipeline_results == "success":
        spinner.succeed("Pipeline execution was successful")
    else:
        spinner.fail("Pipeline execution was unsuccessful")
    spinner.start()
    if not biom_results.get("fail", None):
        spinner.succeed("Biom files had no errors")
    else:
        spinner.fail("Biom files had errors")
        pprint.pprint(biom_results)
    if not network_results.get("fail", None):
        spinner.succeed("Network files had no errors")
    else:
        spinner.fail("Network files had errors")
        pprint.pprint(network_results)
    if not output_results["fail"]:
        spinner.succeed("All modules were executed completely")
    else:
        spinner.fail("All modules were not executed completely")
        pprint.pprint(output_results)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
