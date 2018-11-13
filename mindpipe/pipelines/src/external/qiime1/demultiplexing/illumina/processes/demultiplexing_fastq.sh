#!/usr/bin/env bash
split_libraries_fastq.py -i ${sequences} \
                         -b ${barcodes} \
                         -m ${mappings} \
                         -q ${phred_quality_threshold} \
                         -o \$PWD/

