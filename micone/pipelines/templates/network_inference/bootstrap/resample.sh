#!/usr/bin/env bash

mkdir bootstraps

fastspar_bootstrap \
    --otu_table ${otu_file} \
    --number ${bootstraps} \
    --prefix bootstraps/${meta.id} \
    --threads ${ncpus}

for f in bootstraps/*.tsv; do
    mv -- "\$f" "\${f%.tsv}_otu.boot"
done
