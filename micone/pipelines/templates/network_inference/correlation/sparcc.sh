#!/usr/bin/env bash

fastspar --iterations ${iterations} --yes \
    --otu_table ${otu_file} \
    --correlation ${meta.id}_corr.tsv \
    --covariance ${meta.id}_cov.tsv \
    --threads ${ncpus}

function do_fastspar {
    fastspar --iterations ${iterations} --yes \
        --otu_table \$1 \
        --correlation \${1%_otu.boot}_corr.boot \
        --threads 1
}

export -f do_fastspar

find . -name "*_otu.boot" | parallel -j ${ncpus} do_fastspar
