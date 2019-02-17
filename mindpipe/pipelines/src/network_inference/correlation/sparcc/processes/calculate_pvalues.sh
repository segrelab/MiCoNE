#!/usr/bin/env bash
fastspar_pvalues --otu_table $otu_file \
    --correlation $corr_file \
    --prefix ${id}_boot \
    --permutations $bootstraps \
    --outfile ${level}_pval.tsv
