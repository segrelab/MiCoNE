#!/usr/bin/env python3
from mind.utils import CooccurNet

network = CooccurNet.load_data(
    corr_file="$correlation_file",
    pval_file="$pvalue_file",
    meta_file="$metadata_file",
    lineage_file="$taxondata_file",
    children_file="$childrendata_file",
)
json_str = network.network_json
with open("${id}_${level}_net.json", "w") as fid:
    fid.write(json_str)
