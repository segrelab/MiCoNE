#!/usr/bin/env bash

fastspar --iterations $iterations --yes \
    --otu_table $otu_file \
    --correlation ${otu_file.baseName.split("_otu")[0]}_corr.tsv \
    --covariance ${otu_file.baseName.split("_otu")[0]}_cov.tsv \
    --threads ${ncpus}

for f in *_corr.tsv; do
    mv -- "\$f" "\${f%.tsv}.boot"
done

for f in *_cov.tsv; do
    mv -- "\$f" "\${f%.tsv}.boot"
done
