#!/usr/bin/env bash

mkdir ${id}
cp ${sequence_file} ${id}/sequences.fastq.gz
cp ${barcode_file} ${id}/barcodes.fastq.gz

qiime tools import \
    --type EMPSingleEndSequences \
    --input-path ${id} \
    --output-path ${id}_sequences.qza
