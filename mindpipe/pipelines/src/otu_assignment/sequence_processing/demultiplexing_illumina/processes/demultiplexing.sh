#!/usr/bin/env bash

mkdir ${id}
cp ${sequence_file} ${barcode_file} ${id}/

qiime tools import \
    --type EMPSingleEndSequences \
    --input-path ${id} \
    --output-path ${id}_sequences.qza

qiime demux emp-single \
    --i-seqs ${id}_sequences.qza \
    --m-barcodes-file ${mapping_file} \
    --m-barcodes-column BarcodeSequence \
    --o-per-sample-sequences ${id}_demux.qza

qiime tools export \
    --input-path ${id}_demux.qza \
    --output-path demux_seqs
