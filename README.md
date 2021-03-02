# MiCoNE - Microbial Co-occurrence Network Explorer

![Build Status](https://github.com/segrelab/MiCoNE/workflows/build/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/micone/badge/?version=latest)](https://micone.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/segrelab/MiCoNE/branch/master/graph/badge.svg?token=2tKiI0lUJb)](https://codecov.io/gh/segrelab/MiCoNE)
[![CodeFactor](https://www.codefactor.io/repository/github/segrelab/micone/badge)](https://www.codefactor.io/repository/github/segrelab/micone)
[![Updates](https://pyup.io/repos/github/segrelab/MiCoNE/shield.svg)](https://pyup.io/repos/github/segrelab/MiCoNE/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`MiCoNE`, is a flexible and modular pipeline for 16S data analysis.
It incorporates various popular, publicly available tools as well as custom Python modules and scripts to facilitate inference of co-occurrence networks from 16S data.

<div align="center">
⚠️ <p><strong>The package is under active development and breaking changes are possible</strong></p>
</div>

-   Free software: MIT license
-   Documentation: <https://micone.readthedocs.io/>

Manuscript can be found on [bioRxiv](https://www.biorxiv.org/content/10.1101/2020.09.23.309781v2)

## Features

-   Plug and play architecture: allows easy additions and removal of new tools
-   Flexible and portable: allows running the pipeline on local machine, compute cluster or the cloud with minimal configuration change. Uses the [nextflow](www.nextflow.io) under the hood
-   Parallelization: automatic parallelization both within and across samples (needs to be enabled in the `config` file)
-   Ease of use: available as a minimal `Python` library (without the pipeline) or the full `conda` package

## Installation

Installing the minimal `Python` library:

```sh
pip install micone
```

Installing the `conda` package:

```sh
git clone https://github.com/segrelab/MiCoNE.git
cd MiCoNE
conda env create -n micone -f env.yml
pip install .
```

> NOTE:
> The `conda` package is currently being updated and will be available soon.

## Workflow

![pipeline](assets/pipeline.png)

It supports the conversion of raw 16S sequence data or counts matrices into co-occurrence networks through multiple methods. Each process in the pipeline supports alternate tools for performing the same task, users can use the configuration file to change these values.

## Usage

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

## Configuration

The configuration of the pipeline can be done using a `.toml` file.
The details can be found in the relevant section in the docs.
Here is an example `config` file that performs:

1. grouping of OTUs by taxonomy level
2. correlation of the taxa using `fastspar`
3. calculates p-values
4. constructs the networks

```toml
title = "A example pipeline for testing"

order = """
  otu_processing.filter.group
  otu_processing.export.biom2tsv
  network_inference.bootstrap.resample
  network_inference.correlation.sparcc
  network_inference.bootstrap.pvalue
  network_inference.network.make_network_with_pvalue
"""

output_location = "/home/dileep/Documents/results/sparcc_network"

[otu_processing.filter.group]
  [[otu_processing.filter.group.input]]
    datatype = "otu_table"
    format = ["biom"]
    location = "correlations/good/deblur/deblur.biom"
  [[otu_processing.filter.group.parameters]]
    process = "group"
    tax_levels = "['Family', 'Genus', 'Species']"

[otu_processing.export.biom2tsv]

[network_inference.bootstrap.resample]
  [[network_inference.bootstrap.resample.parameters]]
    process = "resample"
    bootstraps = 10

[network_inference.correlation.sparcc]
  [[network_inference.correlation.sparcc.parameters]]
    process = "sparcc"
    iterations = 5

[network_inference.bootstrap.pvalue]

[network_inference.network.make_network_with_pvalue]
  [[network_inference.network.make_network_with_pvalue.input]]
    datatype = "metadata"
    format = ["json"]
    location = "correlations/good/deblur/deblur_metadata.json"
  [[network_inference.network.make_network_with_pvalue.input]]
    datatype = "computational_metadata"
    format = ["json"]
    location = "correlations/good/deblur/deblur_cmetadata.json"
```

Other example `config` files can be found at `tests/data/pipelines`

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
