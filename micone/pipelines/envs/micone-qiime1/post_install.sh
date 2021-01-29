#!/usr/bin/env bash

set -e

source activate micone-qiime1

pip install h5py==2.8.0
pip install biom-format==2.1.7
pip install qiime
