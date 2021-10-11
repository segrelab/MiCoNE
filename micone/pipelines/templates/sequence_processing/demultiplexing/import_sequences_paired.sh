#!/usr/bin/env bash

mkdir ${meta.id}
cp ${forward_file} ${meta.id}/forward.fastq.gz
cp ${reverse_file} ${meta.id}/reverse.fastq.gz
cp ${barcode_file} ${meta.id}/barcodes.fastq.gz

qiime tools import \
    --type EMPPairedEndSequences \
    --input-path ${meta.id} \
    --output-path ${meta.id}_sequences.qza
