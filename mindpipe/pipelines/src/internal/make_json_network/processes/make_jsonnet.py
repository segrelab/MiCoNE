#!/usr/bin/env python3

from mindpipe import Network

network = Network.load_data(
    interaction_file="$corr_file",
    meta_file="$metadata",
    cmeta_file="$cmetadata",
    obsmeta_file="$obsdata_file",
    pvalue_file="$pval_file",
    children_file="$childrenmap_file",
)
json_str = network.write("${id}_network.json", threshold=False)
