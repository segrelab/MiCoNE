#!/usr/bin/env python3

import pathlib
from typing import List

from micone import Network, NetworkGroup


def main(base_name: str, network_files: List[pathlib.Path]) -> None:
    networks: List[Network] = []
    for network_file in network_files:
        networks.append(Network.load_json(str(network_file)))
    network_group = NetworkGroup(networks)
    pathlib.Path("merged/").mkdir(parents=True, exist_ok=True)
    cids = list(range(len(network_group.contexts)))
    merged_network_group = network_group.combine_pvalues(cids)
    merged_network_group.write(
        "merged/" + base_name + "_network.json", split_files=True
    )


if __name__ == "__main__":
    BASE_NAME = "merged"
    NETWORK_FILES = list(pathlib.Path().glob("*_network.json"))
    main(BASE_NAME, NETWORK_FILES)
