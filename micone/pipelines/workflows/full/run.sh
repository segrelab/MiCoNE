#!/bin/bash -l

# module load miniconda
conda activate micone

nextflow -c nextflow.config run main.nf -resume
