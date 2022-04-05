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
        --covariance \${1%_otu.boot}_cov.boot \
        --threads 1
    rm -f \${1%_otu.boot}_cov.boot
}

export -f do_fastspar

find . -name "*_otu.boot" | parallel -j ${ncpus} do_fastspar
