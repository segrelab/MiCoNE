"""
    Console script for micone
"""

import pathlib
import pprint
from typing import List

import click

from .logging import LOG
from .pipelines import Pipeline
from .setup import Environments
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
def init(ctx, env: str):
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
    "--profile",
    "-p",
    default="local",
    type=str,
    help="The execution profile. Either 'local' or 'sge'",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="The config file that defines the pipeline run",
)
@click.option(
    "--output_location",
    "-o",
    type=click.Path(exists=True),
    default=None,
    help="The base output location to store pipeline results",
)
@click.option(
    "--base_dir",
    "-b",
    type=click.Path(exists=True),
    default=None,
    help="The location of base directory for input files",
)
@click.option(
    "--max_procs",
    "-m",
    type=click.INT,
    default=4,
    help="Maximum number of processes allowed to run in parallel",
)
@click.option(
    "--resume",
    is_flag=True,
    help="The flag to determine whether a previous execution is resumed",
)
@click.pass_context
def run(
    ctx,
    profile: str,
    config: click.Path,
    output_location: click.Path,
    base_dir: click.Path,
    max_procs: int,
    resume: bool,
):
    """Run the pipeline"""
    spinner = ctx.obj["SPINNER"]
    pipeline = Pipeline(
        str(config), profile, str(base_dir), resume, output_location=output_location
    )
    spinner.start()
    spinner.text = "Starting pipeline execution"
    try:
        for process in pipeline.run(max_procs=max_procs):
            if pipeline.process_queue is None:
                raise ValueError("Pipeline process queue is empty")
            process_list = " and ".join(
                [proc.id_.split(".", 2)[-1] for proc in pipeline.process_queue]
            )
            if resume and process.io_exist:
                spinner.start()
                spinner.text = f"Executing {process_list}"
                spinner.succeed(f"Resumed {process}")
            spinner.start()
            spinner.text = f"Executing {process_list}"
            updated_processes = pipeline.wait()
            for proc in updated_processes:
                proc.log()
                if proc.status == "success":
                    spinner.succeed(f"Completed {proc}")
                else:
                    spinner.fail(f"Failed to execute {proc}")
    finally:
        LOG.cleanup()


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="The config file that defines the pipeline run",
)
@click.option(
    "--files", "-f", multiple=True, help="Files can be logs, configs, work, results"
)
@click.pass_context
def clean(ctx, config: click.Path, files: List[str]):
    """Clean files from a pipeline run in the current directory.
    This command irrevesibly deletes content, use with caution
    """
    click.confirm(
        f"Are you sure you want to delete {files} in current directory?", abort=True
    )
    spinner = ctx.obj["SPINNER"]
    spinner.start()
    spinner.text = "Cleaning up pipeline files"
    pipeline = Pipeline(str(config), "local")
    pipeline.clean(files)
    spinner.succeed("Completed cleanup")


@cli.command()
@click.option(
    "--dir", "-d", type=click.Path(exists=True), help="The pipeline execution directory"
)
@click.option(
    "--procs",
    "-p",
    type=click.INT,
    default=4,
    help="Number of processors to use",
)
@click.pass_context
def validate_results(ctx, dir: click.Path, procs: int):
    """Check results of the pipeline execution"""
    pipeline_dir = pathlib.Path(str(dir))
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
