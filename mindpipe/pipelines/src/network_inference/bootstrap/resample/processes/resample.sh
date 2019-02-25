#!/usr/bin/env bash

mkdir bootstraps
cp ${otu_file} bootstraps/

fastspar_bootstrap \
    --otu_table ${otu_file} \
    --number ${bootstraps} \
    --prefix bootstraps/${level}_boot \
    --threads ${threads}
