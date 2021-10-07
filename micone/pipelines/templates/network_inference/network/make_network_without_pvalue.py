#!/usr/bin/env python3

import json

from micone import Network, NetworkGroup


def main(
    base_name: str,
    corr_file: str,
    meta_file: str,
    cmeta_file: str,
    obsmeta_file: str,
    children_file: str,
    interaction_threshold: float,
) -> None:
    network = Network.load_data(
        interaction_file=corr_file,
        meta_file=meta_file,
        cmeta_file=cmeta_file,
        obsmeta_file=obsmeta_file,
        children_file=children_file,
        interaction_threshold=interaction_threshold,
    )
    network.write(base_name + "_network.json")
    network.write(
        base_name + "_thres_network.json", pvalue_filter=False, interaction_filter=True
    )


def create_cmetadata():
    cmetadata = {
        "denoise_cluster": "${meta.denoise_cluster}",
        "chimera_checking": "${meta.chimera_checking}",
        "taxonomy_assignment": "${meta.taxonomy_assignment}",
        "taxonomy_database": "${meta.taxonomy_database}",
        "network_inference": "${meta.network_inference}",
    }
    with open("cmetadata.json", "w") as fid:
        json.dump(cmetadata, fid)


if __name__ == "__main__":
    BASE_NAME = "${meta.id}"
    CORR_FILE = "${corr_file}"
    META_FILE = "${metadata_file}"
    OBSMETA_FILE = "${obs_metadata}"
    CHILDREN_FILE = "${children_map}"
    INTERACTION_THRESHOLD = ${interaction_threshold}
    create_cmetadata()
    CMETA_FILE = "cmetadata.json"
    main(
        BASE_NAME,
        CORR_FILE,
        META_FILE,
        CMETA_FILE,
        OBSMETA_FILE,
        CHILDREN_FILE,
        INTERACTION_THRESHOLD,
    )
