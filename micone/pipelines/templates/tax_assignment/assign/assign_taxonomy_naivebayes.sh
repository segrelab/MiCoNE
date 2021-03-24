#!/usr/bin/env bash

set -e

export TMPDIR=\$PWD

# import reads
qiime tools import \
    --type 'FeatureData[Sequence]' \
    --input-path ${rep_seqs} \
    --output-path rep_seqs.qza

# assign taxonomy to the rep_seqs
qiime feature-classifier classify-sklearn \
    --i-classifier ${params.naive_bayes.classifier} \
    --i-reads rep_seqs.qza \
    --p-n-jobs ${params.naive_bayes.ncpus} \
    --p-confidence ${params.naive_bayes.confidence} \
    --o-classification taxonomy.qza

# export the taxonomy assignment
qiime tools export \
    --input-path taxonomy.qza \
    --output-path taxonomy

cp taxonomy/taxonomy.tsv taxonomy.tsv
