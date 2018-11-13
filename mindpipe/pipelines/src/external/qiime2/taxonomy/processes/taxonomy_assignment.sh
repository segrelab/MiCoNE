#!/usr/bin/env bash
qiime feature-classifier classify-sklearn \
    --i-classifier ${classifier_artifact} \
    --i-reads ${repseq_artifact} \
    --p-n-jobs ${n_jobs} \
    --p-reads-per-batch ${reads_per_batch} \
    --o-classification ${repseq_artifact.baseName}_taxonomy.qza