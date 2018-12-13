"""
    Module that defines the `NetworkGroup` object and methods to read, write and manipulate it
"""

from collections.abc import Collection
import json
from typing import Any, Dict, Iterator, List, Set, Tuple

from .network import Network
from ..utils import JsonEncoder

DType = List[Dict[str, Any]]


class NetworkGroup(Collection):
    """
        Class that represents a group of network objects
        These network objects are intended to be visualized together

        Parameters
        ----------
        networks : List[Network]
            The collection of networks to be grouped
            key = context-id, value = Network

        Attributes
        ----------
        nodes: DType
            The list of nodes in the network group
        links: DType
            The list of links in the network group
        links_thres: DType
            The list of links in the network group after applying thresholds
        contexts: DType
            The list of all contexts in the network group
    """

    def __init__(self, networks: List[Network]) -> None:
        self.nodeid_map: Dict[int, Dict[str, str]] = dict()
        self._networks = networks
        self.nodes, self.links, self.links_thres, self.contexts = self._combine_networks(
            networks
        )

    def __contains__(self, key) -> bool:
        if key in range(len(self)):
            return True
        return False

    def __len__(self) -> int:
        return len(self.contexts)

    def __iter__(self) -> Iterator:
        return iter(self._networks)

    def _combine_nodes(self, all_nodes: Dict[int, DType]) -> DType:
        """ Combine nodes of individual networks into a single list """
        nodes: DType = []
        node_hash: Dict[int, int] = dict()  # taxid => nodes.index
        for cid, network_nodes in all_nodes.items():
            self.nodeid_map[cid] = dict()
            for node in network_nodes:
                if node["taxid"] not in node_hash:
                    id_ = len(nodes)
                    id_old = node["id"]
                    id_new = f"id{id_}"
                    nodes.append(
                        {**node, **{"id": id_new, "children": [], "abundance": None}}
                    )
                    node_hash[node["taxid"]] = id_
                    self.nodeid_map[cid][id_old] = id_new
                else:
                    id_old = node["id"]
                    ind = node_hash[node["taxid"]]
                    id_new = nodes[ind]["id"]
                    self.nodeid_map[cid][id_old] = id_new
        return nodes

    def _combine_links(self, all_links: Dict[int, DType]) -> DType:
        """ Combine links of individual networks into a single list """
        links = []
        for cid, network_links in all_links.items():
            for link in network_links:
                source, target = link["source"], link["target"]
                new_source = self.nodeid_map[cid][source]
                new_target = self.nodeid_map[cid][target]
                links.append(
                    {
                        **link,
                        **{
                            "source": new_source,
                            "target": new_target,
                            "context_index": cid,
                        },
                    }
                )
        return links

    def _combine_networks(
        self, networks: List[Network]
    ) -> Tuple[DType, DType, DType, DType]:
        """
            Combine networks into a network group

            Parameters
            ----------
            networks : List[Network]
                The list of networks to be grouped
                key = context-id, value = Network

            Returns
            -------
            Tuple[DType, DType, DType, DType]
                Nodes, Links, Contexts
        """
        nodes_dict = dict()
        links_dict = dict()
        links_thres_dict = dict()
        contexts = []
        for cid, network in enumerate(networks):
            nodes_dict[cid] = network.nodes
            links_dict[cid] = network.links
            links_thres_dict[cid] = network.links_thres
            context = network.metadata
            contexts.append(context)
        merged_nodes = self._combine_nodes(nodes_dict)
        merged_links = self._combine_links(links_dict)
        merged_links_thres = self._combine_links(links_thres_dict)
        return merged_nodes, merged_links, merged_links_thres, contexts

    def json(self, threshold: bool = True) -> str:
        """ Network group as a JSON string """
        nodes = self.nodes
        if threshold:
            links = self.links_thres
        else:
            links = self.links
        contexts = self.contexts
        network = {"contexts": contexts, "nodes": nodes, "links": links}
        return json.dumps(network, indent=2, sort_keys=True, cls=JsonEncoder)

    def write(self, fpath: str, threshold: bool = True) -> None:
        """
            Write network group to file as JSON

            Parameters
            ----------
            fpath : str
                The path to the `JSON` file
            threshold : bool, optional
                True if threshold needs to applied to links before writing to file
        """
        with open(fpath, "w") as fid:
            fid.write(self.json(threshold=threshold))

    # TODO:
    # def load_data: Loads from files or one group file?
