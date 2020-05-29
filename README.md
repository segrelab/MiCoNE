MiCoNE - Microbial Co-occurrence Network Explorer
=================================================

[![Build Status](https://travis-ci.com/dileep-kishore/mindpipe.svg?token=qCMKydrUTvcJ87J6czex&branch=master)](https://travis-ci.com/dileep-kishore/mindpipe)
[![CodeFactor](https://www.codefactor.io/repository/github/dileep-kishore/mindpipe/badge)](https://www.codefactor.io/repository/github/dileep-kishore/mindpipe)
[![Updates](https://pyup.io/repos/github/dileep-kishore/mindpipe/shield.svg?token=15e74ba4-b27a-4709-99cf-96bcf698e33b)](https://pyup.io/repos/github/dileep-kishore/mindpipe/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`MiCoNE`, is a flexible and modular pipeline for 16S data analysis. It incorporates various popular, publicly available tools as well as custom Python modules and scripts to facilitate inference of co-occurrence networks from 16S data.

-   Free software: MIT license
-   Documentation: <https://dileep-kishore.github.io/mindpipe>.

Manuscript in preparation.

Features
--------

- Plug and play architecture: allows easy additions and removal of new tools
- Flexible and portable: allows running the pipeline on local machine, compute cluster or the cloud with minimal configuration change. Uses the [nextflow](www.nextflow.io) under the hood
- Parallelization: automatic parallelization both within and across samples
- Ease of use: available as `conda` package as well as a `docker` container

Workflow
--------

![pipeline](assets/pipeline.png)

It supports the conversion of raw 16S sequence data or counts matrices into co-occurrence networks through multiple methods. Each process in the pipeline supports alternate tools for performing the same task, users can use the configuration file to change these values.

Usage
-----

The `MiCoNE` pipelines comes with an easy to use CLI. To get a list of subcommands you can type:

```bash
micone --help
```

Supported subcommands:
1. `init` - Creates `conda` environments for various pipeline processes
2. `run` - The main subcommand that runs the pipeline
3. `clean` - Cleans temporary data, log files and other extraneous files

To run the pipeline:

```bash
micone run -p local -c run.toml -m 4
```

This runs the pipeline in the `local` machine using `run.toml` for the pipeline configuration and with a maximum of 4 processes in parallel at a time.

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
