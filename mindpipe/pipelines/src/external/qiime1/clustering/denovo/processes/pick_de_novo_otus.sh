#!/usr/bin/env bash

pick_de_novo_otus.py -i ${sequence_list} \
                     -a -O ${ncpus} \
                     -p ${parameters} \
                     -f -o \$PWD/

