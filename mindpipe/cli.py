"""
    Console script for mindpipe
"""

import click
from halo import Halo

from .logging import LOG
from .pipelines import Pipeline
from .setup import Environments


@click.group()
@click.option(
    "--log", "-l", default=False, type=bool, help="Flag to turn on/off logging"
)
@click.pass_context
def cli(ctx, log):
    """ Main entry point to mindpipe """
    spinner = Halo(text="Starting up...", spinner="dots")
    spinner.start()
    ctx.obj["SPINNER"] = spinner
    spinner.succeed("Successfully initialized mindpipe")
    if log:
        LOG.enable("mindpipe")


@cli.command()
@click.option(
    "--env",
    "-e",
    default=None,
    help="The environment to initialize. By default will initialize all",
)
@click.pass_context
def init(ctx, env):
    """ Initialize the package and environments """
    spinner = ctx.obj["SPINNER"]
    environments = Environments()
    for env_cmd in environments.init(env):
        spinner.start()
        spinner.text = f"Initializing environment: {env_cmd}"
        env_cmd.wait()
        if env_cmd.status == "failure":
            spinner.fail(f"{env_cmd} Failed")
        elif env_cmd.status == "success":
            spinner.succeed(f"{env_cmd} Passed")
    for post_cmd in environments.post_install(env):
        spinner.start()
        spinner.text = f"Running post installation: {post_cmd}"
        post_cmd.wait()
        if post_cmd.status == "failure":
            spinner.fail(f"{post_cmd} Failed")
        elif post_cmd.status == "success":
            spinner.succeed(f"{post_cmd} Passed")


@cli.command()
@click.option(
    "--profile",
    "-p",
    default="local",
    type=str,
    help="The execution profile. Either 'local' or 'qsub'",
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
@click.pass_context
def run(ctx, profile, config, output_location, base_dir):
    """ Run the pipeline """
    spinner = ctx.obj["SPINNER"]
    pipeline = Pipeline(config, profile, base_dir, output_location=output_location)
    spinner.start()
    spinner.text = "Starting pipeline execution"
    for process in pipeline.run():
        spinner.start()
        spinner.text = f"Executing {process} process"
        process.wait()
        if process.status == "success":
            spinner.succeed(f"Finished executing {process}")
        else:
            spinner.fail(f"Failed to execute {process}")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
