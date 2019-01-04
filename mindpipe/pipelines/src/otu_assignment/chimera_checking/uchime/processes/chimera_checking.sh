#!/usr/bin/env bash

qiime vsearch uchime-denovo \
  --i-table atacama-table.qza \
  --i-sequences atacama-rep-seqs.qza \
  --output-dir uchime-dn-out

qiime feature-table filter-features \
  --i-table atacama-table.qza \
  --m-metadata-file uchime-dn-out/nonchimeras.qza \
  --o-filtered-table uchime-dn-out/table-nonchimeric-wo-borderline.qza
qiime feature-table filter-seqs \
  --i-data atacama-rep-seqs.qza \
  --m-metadata-file uchime-dn-out/nonchimeras.qza \
  --o-filtered-data uchime-dn-out/rep-seqs-nonchimeric-wo-borderline.qza
qiime feature-table summarize \
  --i-table uchime-dn-out/table-nonchimeric-wo-borderline.qza \
  --o-visualization uchime-dn-out/table-nonchimeric-wo-borderline.qzv
