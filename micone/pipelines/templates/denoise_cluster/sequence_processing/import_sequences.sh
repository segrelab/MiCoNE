#!/usr/bin/env bash

mkdir ${meta.id}
cp ${sequence_file} ${meta.id}/sequences.fastq.gz
cp ${barcode_file} ${meta.id}/barcodes.fastq.gz

qiime tools import \
    --type EMPSingleEndSequences \
    --input-path ${meta.id} \
    --output-path ${meta.id}_sequences.qza
