#!/usr/bin/env bash

set -e

qiime vsearch uchime-denovo \
  --i-table ${otutable_artifact} \
  --i-sequences ${repseqs_artifact} \
  --output-dir output

qiime feature-table filter-features \
  --i-table ${otutable_artifact} \
  --m-metadata-file output/nonchimeras.qza \
  --o-filtered-table otu_table_nonchimeric.qza

qiime feature-table filter-seqs \
  --i-data ${repseqs_artifact} \
  --m-metadata-file output/nonchimeras.qza \
  --o-filtered-data rep_seqs_nonchimeric.qza
