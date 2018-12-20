#!/usr/bin/env bash

pick_closed_reference_otus.py \
  -i ${sequence_file} \
  -a -O ${ncpus} \
  -r ${sequence_reference} \
  -t ${taxonomy_mapping} \
  -p ${parameters} \
  -f -o \$PWD/
