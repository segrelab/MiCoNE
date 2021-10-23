#!/usr/bin/env python3

import json

from micone import Network


def main(
    base_name: str,
    corr_file: str,
    meta_file: str,
    cmeta_file: str,
    obsmeta_file: str,
    pvalue_file: str,
    children_file: str,
    interaction_threshold: float,
    pvalue_threshold: float,
) -> None:
    network = Network.load_data(
        interaction_file=corr_file,
        meta_file=meta_file,
        cmeta_file=cmeta_file,
        obsmeta_file=obsmeta_file,
        pvalue_file=pvalue_file,
        children_file=children_file,
        interaction_threshold=interaction_threshold,
        pvalue_threshold=pvalue_threshold,
    )
    network.write(base_name + "_network.json")
    # network.write(
    #     base_name + "_network_thres.json", pvalue_filter=True, interaction_filter=True
    # )


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
    PVALUE_FILE = "${pvalue_file}"
    META_FILE = "${metadata_file}"
    if not META_FILE:
        raise ValueError(
            "The metadata file needs to be supplied via network.config in make_network_with_pvalue"
        )
    OBSMETA_FILE = "${obs_metadata}"
    CHILDREN_FILE = "${children_map}"
    INTERACTION_THRESHOLD = float("${interaction_threshold}")
    PVALUE_THRESHOLD = float("${pvalue_threshold}")
    create_cmetadata()
    CMETA_FILE = "cmetadata.json"
    main(
        BASE_NAME,
        CORR_FILE,
        META_FILE,
        CMETA_FILE,
        OBSMETA_FILE,
        PVALUE_FILE,
        CHILDREN_FILE,
        INTERACTION_THRESHOLD,
        PVALUE_THRESHOLD,
    )
