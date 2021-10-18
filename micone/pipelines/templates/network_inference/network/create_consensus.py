#!/usr/bin/env python3

import pathlib
from typing import List

from micone import Network, NetworkGroup


def main(
    base_name: str,
    network_files: List[pathlib.Path],
    method: str,
    parameter: float,
    pvalue_filter: bool,
    interaction_filter: bool,
) -> None:
    networks: List[Network] = []
    for network_file in network_files:
        networks.append(Network.load_json(str(network_file)))
    network_group = NetworkGroup(networks)
    pathlib.Path("consensus/").mkdir(parents=True, exist_ok=True)
    cids = list(range(len(network_group.contexts)))
    filtered_network_group = network_group.filter(
        pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
    )
    consensus_network_group = filtered_network_group.get_consensus_network(
        cids, method=method, parameter=parameter
    )
    consensus_network_group.write("consensus/" + base_name + "_network.json")


if __name__ == "__main__":
    BASE_NAME = "consensus"
    METHOD = "${method}"
    PARAMETER = float("${parameter}")
    PVALUE_FILTER = True if "${pvalue_filter}" == "true" else False
    INTERACTION_FILTER = True if "${interaction_filter}" == "true" else False
    NETWORK_FILES = list(pathlib.Path().glob("*_network.json"))
    main(BASE_NAME, NETWORK_FILES, METHOD, PARAMETER, PVALUE_FILTER, INTERACTION_FILTER)
