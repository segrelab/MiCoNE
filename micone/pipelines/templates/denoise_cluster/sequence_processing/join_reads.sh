#!/usr/bin/env bash

join_paired_ends.py \
    -f ${sequence_files[0]} \
    -r ${sequence_files[1]} \
    -b ${barcode_file} \
    --min_overlap ${min_overlap} \
    --perc_max_diff ${perc_max_diff} \
    --output_dir joined_reads \

gzip joined_reads/fastqjoin.join.fastq
mv joined_reads/fastqjoin.join.fastq.gz joined_reads/${sequence_files[0].baseName.split('_forward')[0]}_reads.fastq.gz

gzip joined_reads/fastqjoin.join_barcodes.fastq
mv joined_reads/fastqjoin.join_barcodes.fastq.gz joined_reads/${barcode_file.getSimpleName()}.fastq.gz
