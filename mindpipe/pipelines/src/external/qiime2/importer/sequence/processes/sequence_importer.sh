#!/usr/bin/env bash

qiime tools import \
    --type $input_type \
    --input-path $sequence_folder \
    --output-path ${sequence_folder.baseName}_sequences.qza
