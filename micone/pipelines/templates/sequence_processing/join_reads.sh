#!/usr/bin/env bash

qiime vsearch join-pairs \
  --i-demultiplexed-seqs ${demux_artifact} \
  --o-joined-sequences ${meta.id}_joined.qza
