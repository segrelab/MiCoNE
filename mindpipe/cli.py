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
    spinner.succeed("Successfully initialized mindpipe")
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
    spinner.start()
    environments = Environments()
    for env_cmd in environments.init(env):
        spinner.text = f"Initializing environment: {env_cmd.cmd}"
        env_cmd.wait()
        if env_cmd.error:
            spinner.fail(f"{env_cmd} failed")
    spinner.succeed("Initialized all requested environments")
    spinner.start()
    for post_cmd in environments.post_install(env):
        spinner.text = f"Running post installation: {post_cmd.cmd}"
        post_cmd.wait()
        if post_cmd.error:
            spinner.fail(f"{post_cmd} failed")
    spinner.succeed("Post installation successful for all requested environments")


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
    Pipeline(config)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
