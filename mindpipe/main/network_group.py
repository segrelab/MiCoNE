"""
    Module that defines the `NetworkGroup` object and methods to read, write and manipulate it
"""

from collections.abc import Collection
from typing import Any, Dict, Iterator, List, Union

import networkx as nx
import simplejson

from .network import Network

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
        graph : Union[nx.MultiGraph, nx.MultiDiGraph]
            The networkx multi-graph representation of the network
        nodes: DType
            The list of nodes in the network group
        links: DType
            The list of links in the network group
        contexts: DType
            The list of all contexts in the network group
    """

    def __init__(self, networks: List[Network]) -> None:
        self.nodeid_map: Dict[int, Dict[str, str]] = dict()
        self._networks = networks
        if not networks or [n for n in networks if not isinstance(n, Network)]:
            raise ValueError(
                "The networks parameter must be a list of one or more networks"
            )
        self.graph = self._combine_networks(networks)

    def __contains__(self, key) -> bool:
        if key in range(len(self)):
            return True
        return False

    def __len__(self) -> int:
        return len(self._networks)

    def __iter__(self) -> Iterator:
        return iter(self._networks)

    def __repr__(self) -> str:
        n_nodes = len(self.nodes)
        n_links = len(self.links)
        n_contexts = len(self.contexts)
        return f"<NetworkGroup contexts={n_contexts} nodes={n_nodes} links={n_links}>"

    def _combine_nodes(self, all_nodes: Dict[int, DType]) -> DType:
        """ Combine nodes of individual networks into a single list """
        nodes: DType = []
        node_hash: Dict[int, int] = dict()  # taxid => nodes.index
        if len(all_nodes) == 1:
            return all_nodes[0]
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
        if len(all_links) == 1:
            return all_links[0]
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
    ) -> Union[nx.MultiGraph, nx.MultiDiGraph]:
        """
            Combine networks into a network group

            Parameters
            ----------
            networks : List[Network]
                The list of networks to be grouped

            Returns
            -------
            Union[nx.MultiGraph, nx.MultiDiGraph]
                The networkx graph of the network
        """
        nodes_dict = dict()
        links_dict = dict()
        contexts = []
        for cid, network in enumerate(networks):
            nodes_dict[cid] = network.nodes
            links_dict[cid] = network.links
            contexts.append(network.metadata)
        merged_nodes = self._combine_nodes(nodes_dict)
        merged_links = self._combine_links(links_dict)
        if all([n.graph.is_directed() for n in networks]):
            graph = nx.MultiDiGraph(contexts=contexts)
        else:
            graph = nx.MultiGraph(contexts=contexts)
        for node in merged_nodes:
            graph.add_node(node["id"], **node)
        for link in merged_links:
            graph.add_edge(link["source"], link["target"], **link)
        return graph

    @property
    def nodes(self) -> DType:
        """ The list of nodes in the `NetworkGroup` and their corresponding properties """
        return [data for _, data in self.graph.nodes(data=True)]

    @property
    def links(self) -> DType:
        """ The list of links in the `NetworkGroup` and their corresponding properties """
        return [data for _, _, data in self.graph.edges(data=True)]

    @property
    def contexts(self) -> DType:
        """ The contexts for the group of networks """
        return [md for md in self.graph.graph]

    @property
    def filtered_links(self) -> DType:
        """
            The links of the networks after applying filtering

            Returns
            -------
            List[Dict[str, Any]]
                The list of links in the network after applying a threshold
        """
        filtered_links_dict = dict()
        if len(self.contexts) > 1:
            for cid, network in enumerate(self._networks):
                filtered_links_dict[cid] = network.filtered_links
            merged_filtered_links = self._combine_links(filtered_links_dict)
        else:
            network = self._networks[0]
            merged_filtered_links = network.filtered_links
        return merged_filtered_links

    def json(self, threshold: bool = True) -> str:
        """ Network group as a JSON string """
        nodes = self.nodes
        if threshold:
            links = self.filtered_links
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

    @classmethod
    def load_json(cls, fpath: str) -> "NetworkGroup":
        """
            Create a `NetworkGroup` object from network `JSON` file

            Parameters
            ----------
            fpath : str
                The path to the network `JSON` file

            Returns
            -------
            NetworkGroup
                The instance of the `NetworkGroup` class
        """
        with open(fpath, "r") as fid:
            raw_data = simplejson.load(fid)
        n_networks = len(raw_data["contexts"])
        all_node_dict = {n["id"]: n for n in raw_data["nodes"]}
        data_dict: Dict[int, dict] = {
            n: {"nodes": [], "links": [], "metadata": {}} for n in range(n_networks)
        }
        unique_name_dict: Dict[int, dict] = {
            n: {"nodes": set(), "links": set()} for n in range(n_networks)
        }
        for cid in range(n_networks):
            data_dict[cid]["metadata"] = {**raw_data["contexts"][cid]}
        for link in raw_data["links"]:
            link_cid = link["context_index"]
            source = all_node_dict[link["source"]]
            source_name = link["source"]
            target = all_node_dict[link["target"]]
            target_name = link["target"]
            if (
                f"{source_name}-{target_name}"
                not in unique_name_dict[link_cid]["links"]
            ):
                data_dict[link_cid]["links"].append(link)
                unique_name_dict[link_cid]["links"].add(f"{source_name}-{target_name}")
            else:
                print("new link", link)
            if source_name not in unique_name_dict[link_cid]["nodes"]:
                data_dict[link_cid]["nodes"].append(source)
                unique_name_dict[link_cid]["nodes"].add(source_name)
            if target_name not in unique_name_dict[link_cid]["nodes"]:
                data_dict[link_cid]["nodes"].append(target)
                unique_name_dict[link_cid]["nodes"].add(target_name)
        networks: List[Network] = []
        print("all nodes", len(all_node_dict))
        print("node_set", len(unique_name_dict[0]["nodes"]))
        print("link_set", len(unique_name_dict[0]["links"]))
        for cid in range(n_networks):
            metadata = data_dict[cid]["metadata"]
            nodes = data_dict[cid]["nodes"]
            links = data_dict[cid]["links"]
            network_raw_data = {**metadata, "nodes": nodes, "links": links}
            networks.append(Network.load_json(raw_data=network_raw_data))
        return cls(networks)
