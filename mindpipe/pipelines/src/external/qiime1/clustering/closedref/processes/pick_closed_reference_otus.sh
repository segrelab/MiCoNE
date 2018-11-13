#!/usr/bin/env bash

pick_closed_reference_otus.py -i ${sequence_list} \
                              -a -O ${ncpus} \
                              -r ${references} \
                              -t ${taxonomy} \
                              -p ${parameters} \
                              -f -o \$PWD/

