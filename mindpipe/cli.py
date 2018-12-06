"""
    Console script for mindpipe
"""

import click
from halo import Halo

from .pipelines import Pipeline
from .setup import Environments


@click.group()
@click.pass_context
def cli(ctx):
    """ Main entry point to mindpipe """
    spinner = Halo(text="Starting up...", spinner="dots")
    spinner.start()
    ctx.obj["SPINNER"] = spinner
    return None


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
    spinner.text = "Initializing environment: "
    environments = Environments()
    environments.init(env)


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
@click.pass_context
def run(ctx, profile, config):
    """ Run the pipeline """
    ctx.obj["PROFILE"] = profile
    pipeline = Pipeline(config)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
