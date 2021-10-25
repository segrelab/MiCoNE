#!/usr/bin/env bash

qiime demux emp-paired \
    --i-seqs ${sequence_artifact} \
    --m-barcodes-file ${mapping_file} \
    --m-barcodes-column ${barcode_column} \
    ${rcb} \
    ${rcmb} \
    --o-per-sample-sequences ${meta.id}_demux.qza \
    --o-error-correction-details ${meta.id}_error.qza
