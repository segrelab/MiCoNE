#!/usr/bin/env bash

qiime demux emp-single \
    --i-seqs ${id}_sequences.qza \
    --m-barcodes-file ${mapping_file} \
    --m-barcodes-column BarcodeSequence \
    ${rcb} \
    ${rcmb} \
    --o-per-sample-sequences ${id}_demux.qza
