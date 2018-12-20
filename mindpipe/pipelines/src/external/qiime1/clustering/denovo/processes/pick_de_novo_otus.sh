#!/usr/bin/env bash

pick_de_novo_otus.py \
  -i ${sequence_file} \
  -a -O ${ncpus} \
  -p ${parameters} \
  -f -o \$PWD/
