#!/usr/bin/env python3

from mindpipe import Network

network = Network.load_data(
    interaction_file="$correlation_file",
    meta_file="$metadata_file",
    cmeta_file="$cmetadata_file",
    obsmeta_file="$obsdata_file",
    pvalue_file="$pvalue_file",
    children_file="$childrendata_file",
)
json_str = network.write("${id}_${level}_net.json", threshold=False)
