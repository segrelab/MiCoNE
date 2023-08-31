#!/bin/bash -l

# NOTE: You will need to replace the data/ folder with the data folder from
# Zenodo (data.zip) if you want to use all taxonomy databases and classifiers
# wget "https://zenodo.org/record/7051556/files/data.zip?download=1"

# module load miniconda
conda activate micone

nextflow -c nextflow.config run main.nf -resume
