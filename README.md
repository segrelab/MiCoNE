# MiCoNE - Microbial Co-occurrence Network Explorer

![Build Status](https://github.com/segrelab/MiCoNE/workflows/build/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/micone/badge/?version=latest)](https://micone.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/segrelab/MiCoNE/branch/master/graph/badge.svg?token=2tKiI0lUJb)](https://codecov.io/gh/segrelab/MiCoNE)
[![CodeFactor](https://www.codefactor.io/repository/github/segrelab/micone/badge)](https://www.codefactor.io/repository/github/segrelab/micone)
[![Updates](https://pyup.io/repos/github/segrelab/MiCoNE/shield.svg)](https://pyup.io/repos/github/segrelab/MiCoNE/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`MiCoNE` is a Python package for the exploration of the effects of various possible tools used during the 16S data processing workflow on the inferred co-occurrence networks.
It is also developed as a flexible and modular pipeline for 16S data analysis, offering parallelized, fast and reproducible runs executed for different combinations of tools for each step of the data processing workflow.
It incorporates various popular, publicly available tools as well as custom Python modules and scripts to facilitate inference of co-occurrence networks from 16S data.

- Free software: MIT license
- Documentation: <https://micone.readthedocs.io/>

Manuscript can be found on [bioRxiv](https://www.biorxiv.org/content/10.1101/2020.09.23.309781v2) (to be updated with link to publication).

## Features

- Plug and play architecture: allows easy additions and removal of new tools
- Flexible and portable: allows running the pipeline on local machine, compute cluster or the cloud with minimal configuration change through the usage of [nextflow](www.nextflow.io)
- Parallelization: automatic parallelization both within and across samples (needs to be enabled in the `nextflow.config` file)
- Ease of use: available as a minimal `Python` library (without the pipeline) or as a full `conda` package

## Installation

Installing the minimal `Python` library:

```sh
pip install micone
```

Installing the `conda` package:

```sh
git clone https://github.com/segrelab/MiCoNE.git
cd MiCoNE
# Here we use mamba, you can also use conda
mamba env create -n micone -f env.yml
```

> NOTE:
> Direct installation via anaconda cloud will be available soon.


## Workflow

![pipeline](assets/pipeline.png)

It supports the conversion of raw 16S sequence data into co-occurrence networks.
Each process in the pipeline supports alternate tools for performing the same task, users can use the configuration file to change these values.

## Usage (needs to be updated)

The `MiCoNE` pipelines comes with an easy-to-use CLI. To get a list of subcommands you can type:

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

## Configuration (needs to be updated)

The configuration of the pipeline can be done using a `.toml` file.
The details can be found in the relevant section in the docs.
Here is an example `config` file that performs:

1. grouping of OTUs by taxonomy level
2. correlation of the taxa using `fastspar`
3. calculates p-values
4. constructs the networks

```sh
Coming soon
```

Other example `config` files can be found at `tests/data/pipelines`

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
