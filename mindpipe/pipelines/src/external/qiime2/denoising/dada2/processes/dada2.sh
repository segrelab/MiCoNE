#!/usr/bin/env bash

qiime dada2 denoise-${itype} \
    --i-demultiplexed-seqs $sequence_artifact \
    --p-n-threads $n_threads \
    --p-max-ee $max_ee \
    --p-trunc-q $trunc_q \
    ${trim_cmd} \
    --o-representative-sequences dada2_rep_seqs.qza \
    --o-table dada2_table.qza
