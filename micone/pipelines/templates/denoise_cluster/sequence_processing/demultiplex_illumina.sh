#!/usr/bin/env bash

qiime demux emp-single \
    --i-seqs ${sequence_artifact} \
    --m-barcodes-file ${mapping_file} \
    --m-barcodes-column BarcodeSequence \
    ${rcb} \
    ${rcmb} \
    --o-per-sample-sequences ${meta.id}_demux.qza
