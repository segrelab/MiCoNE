#!/usr/bin/env python3

from micone import Network, NetworkGroup


def main(
    base_name: str,
    corr_file: str,
    meta_file: str,
    cmeta_file: str,
    obsmeta_file: str,
    pvalue_file: str,
    children_file: str,
) -> None:
    network = Network.load_data(
        interaction_file=corr_file,
        meta_file=meta_file,
        cmeta_file=cmeta_file,
        obsmeta_file=obsmeta_file,
        pvalue_file=pvalue_file,
        children_file=children_file,
        interaction_threshold=0.2,
        pvalue_threshold=0.05,
    )
    network_group = NetworkGroup([network])
    network_group.write(base_name + "_network.json")
    network_group.write(
        base_name + "_thres_network.json", pvalue_filter=False, interaction_filter=True
    )


if __name__ == "__main__":
    BASE_NAME = "${level}"
    CORR_FILE = "${corr_file}"
    META_FILE = "${metadata}"
    CMETA_FILE = "$cmetadata"
    OBSMETA_FILE = "$obsdata_file"
    PVALUE_FILE = "$pval_file"
    CHILDREN_FILE = "$childrenmap_file"
    main(
        BASE_NAME,
        CORR_FILE,
        META_FILE,
        CMETA_FILE,
        OBSMETA_FILE,
        PVALUE_FILE,
        CHILDREN_FILE,
    )
