#!/usr/bin/env bash
fastspar_pvalues --otu_table $otu_file \
    --correlation $corr_file \
    --prefix $id \
    --permutations $bootstraps \
    --outfile ${id}_pval.tsv
