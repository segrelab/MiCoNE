#!/usr/bin/env bash

mkdir corr_bootstraps
mv *.boot corr_bootstraps

BOOTSTRAPS=\$(ls -1 corr_bootstraps | wc -l)

fastspar_pvalues --otu_table ${otu_file} \
    --correlation ${corr_file} \
    --prefix corr_bootstraps/ \
    --permutations \$BOOTSTRAPS \
    --outfile ${meta.id}_pval.tsv \
    --threads ${ncpus}
