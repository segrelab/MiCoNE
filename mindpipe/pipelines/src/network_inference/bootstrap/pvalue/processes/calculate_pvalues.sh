#!/usr/bin/env bash

mkdir corr_bootstraps
mv *_boot_*_corr.tsv corr_bootstraps

OTU_FILE=${level_str}.tsv
CORR_FILE=${level_str}_corr.tsv
BOOTSTRAPS=\$(ls -1 corr_bootstraps | wc -l)

fastspar_pvalues --otu_table \$OTU_FILE \
    --correlation \$CORR_FILE \
    --prefix corr_bootstraps/${level_str}_boot \
    --permutations \$BOOTSTRAPS \
    --outfile ${level_str}_pval.tsv \
    --threads ${threads}
