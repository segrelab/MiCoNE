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
    "--log", "-l", default=True, type=bool, help="Flag to turn on/off logging"
)
@click.pass_context
def cli(ctx, log):
    """ Main entry point to mindpipe """
    spinner = Halo(text="Starting up...", spinner="dots")
    spinner.start()
    ctx.obj["SPINNER"] = spinner
    spinner.succeed("Successfully initialized mindpipe")
    if log:
        LOG.enable()


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
@click.option(
    "--resume",
    is_flag=True,
    help="The flag to determine whether a previous execution is resumed",
)
@click.pass_context
def run(ctx, profile, config, output_location, base_dir, resume):
    """ Run the pipeline """
    spinner = ctx.obj["SPINNER"]
    pipeline = Pipeline(
        config, profile, base_dir, resume, output_location=output_location
    )
    spinner.start()
    spinner.text = "Starting pipeline execution"
    try:
        for process in pipeline.run():
            spinner.start()
            spinner.text = f"Executing {process} process"
            if resume and process.io_exist:
                spinner.succeed(f"Resumed {process}")
            else:
                process.wait()
                process.log()
                if process.status == "success":
                    spinner.succeed(f"Finished executing {process}")
                else:
                    spinner.fail(f"Failed to execute {process}")
    finally:
        click.secho(f"Log file is at {LOG.path}")
        LOG.cleanup()


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
