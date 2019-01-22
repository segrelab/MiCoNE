#!/usr/bin/env bash

# import reads
qiime tools import \
    --type 'FeatureData[Sequence]' \
    --input-path ${rep_seqs} \
    --output-path rep_seqs.qza

# assign taxonomy to the rep_seqs
qiime feature-classifier classify-sklearn \
    --i-classifier ${classifier} \
    --i-reads rep_seqs.qza \
    --p-n-jobs ${ncpus} \
    --p-reads-per-batch ${read_per_batch} \
    --p-confidence ${confidence} \
    --o-classification taxonomy.qza

# export the taxonomy assignment
qiime tools export \
    --input-path taxonomy.qza \
    --output-path taxonomy

cp taxonomy/taxonomy.tsv taxonomy.tsv
