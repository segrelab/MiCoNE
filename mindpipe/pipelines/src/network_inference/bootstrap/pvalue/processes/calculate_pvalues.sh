#!/usr/bin/env bash

mkdir corr_bootstraps
mv *_boot_*_corr.boot corr_bootstraps

BOOTSTRAPS=\$(ls -1 corr_bootstraps | wc -l)

fastspar_pvalues --otu_table $otu_file \
    --correlation $corr_file \
    --prefix corr_bootstraps/${level}_boot \
    --permutations \$BOOTSTRAPS \
    --outfile ${level}_pval.tsv \
    --threads ${ncpus}
