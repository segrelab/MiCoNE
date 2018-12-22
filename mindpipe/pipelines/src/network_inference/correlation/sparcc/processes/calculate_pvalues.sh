#!/usr/bin/env bash
fastspar_pvalues --otu_table $otu_file \
    --correlation $corr_file \
    --prefix ${id}_boot \
    --permutations $bootstraps \
    --outfile ${id}_pval.tsv
