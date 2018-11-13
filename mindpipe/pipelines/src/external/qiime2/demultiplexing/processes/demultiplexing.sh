#!/usr/bin/env bash

qiime demux emp-${itype} \
    --i-seqs $sequence_artifact \
    --m-barcodes-file $barcodes_file \
    --m-barcodes-column $barcodes_column \
    $rcb \
    $rcmb \
    --o-per-sample-sequences ${fname}_demux.qza \
    --output-dir raw_output
