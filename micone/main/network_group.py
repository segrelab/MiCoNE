"""
    Module that defines the `NetworkGroup` object and methods to read, write and manipulate it
"""

from collections.abc import Collection
from itertools import product
from typing import Any, Dict, Iterator, List, Union

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, chi2
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

    def __add__(self, other: "NetworkGroup") -> "NetworkGroup":
        """Combine two `NetworkGroup` objects and return a new `NetworkGroup` object
        The new `NetworkGroup` contains nodes and edges from both the input objects
        """
        networks = [*self._networks, *other._networks]
        return NetworkGroup(networks)

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
            for link in all_links[0]:
                links.append({**link, "context_index": 0})
            return links
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
        return self.graph.graph["contexts"]

    def get_adjacency_vectors(self, key: str) -> List[pd.Series]:
        """
        Returns the adjacency matrix for each context as a `pd.Series`

        Parameters
        ----------
        key : str
            The `edge` property to be used to contruct the vectors

        Returns
        -------
        List[pd.Series]:
            The list of adjacency vectors
        """
        ids = list(self.nodes)
        size = len(ids) * len(ids)
        index = [f"{id1}-{id2}" for id1, id2 in product(ids, repeat=2)]
        adj_vector_list: List[pd.Series] = [
            pd.Series(np.zeros((size), dtype=float), index=index)
        ]
        graph = self.graph
        for source, target, data in graph.edges(data=True):
            cid = data["cid"]
            id_ = f"{source}-{target}"
            adj_vector_list[cid][id_] = data[key]
        return adj_vector_list

    def update_thresholds(
        self, interaction_threshold: float = 0.3, pvalue_threshold: float = 0.05
    ) -> None:
        """Update the thresholds on the networks

        Parameters
        ----------
        interaction_threshold : float, optional
            The value to which the interactions (absolute value) are to be thresholded
            To disable thresholding based on interaction value then pass in 0.0
            Default value is 0.3
        pvalue_threshold : float, optional
            This is the `alpha` value for pvalue cutoff
            Default value is 0.05
        """
        for network in self._networks:
            network.interaction_threshold = interaction_threshold
            network.pvalue_threshold = pvalue_threshold

    def filter_links(self, pvalue_filter: bool, interaction_filter: bool) -> DType:
        """
        The links of the networks after applying filtering

        Parameters
        ----------
        pvalue_filter : bool
            If True will use `pvalue_threshold` for filtering
        interaction_filter : bool
            If True will use `interaction_threshold` for filtering

        Returns
        -------
        DType
            The list of links in the network after applying thresholds
        """
        filtered_links_dict = dict()
        for cid, network in enumerate(self._networks):
            filtered_links_dict[cid] = network.filter_links(
                pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
            )
        merged_filtered_links = self._combine_links(filtered_links_dict)
        return merged_filtered_links

    def json(
        self, pvalue_filter: bool = False, interaction_filter: bool = False
    ) -> str:
        """
        Returns the network as a `JSON` string

        Parameters
        ----------
        pvalue_filter : bool
            If True will use `pvalue_threshold` for filtering
            Default  value is False
        interaction_filter : bool
            If True will use `interaction_threshold` for filtering
            Default  value is False

        Returns
        -------
        str
            The `JSON` string representation of the network
        """
        nodes = self.nodes
        links = self.filter_links(
            pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
        )
        contexts = self.contexts
        network = {"contexts": contexts, "nodes": nodes, "links": links}
        return simplejson.dumps(network, indent=2, sort_keys=True, ignore_nan=True)

    def write(
        self, fpath: str, pvalue_filter: bool = False, interaction_filter: bool = False
    ) -> None:
        """
        Write network to file as JSON

        Parameters
        ----------
        fpath : str
            The path to the `JSON` file
        pvalue_filter : bool
            If True will use `pvalue_threshold` for filtering
            Default  value is False
        interaction_filter : bool
            If True will use `interaction_threshold` for filtering
            Default  value is False
        """
        with open(fpath, "w") as fid:
            fid.write(
                self.json(
                    pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
                )
            )

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
        unique_node_dict: Dict[int, dict] = {n: set() for n in range(n_networks)}
        for cid in range(n_networks):
            data_dict[cid]["metadata"] = {**raw_data["contexts"][cid]}
        for link in raw_data["links"]:
            link_cid = link["context_index"]
            source = all_node_dict[link["source"]]
            source_name = link["source"]
            target = all_node_dict[link["target"]]
            target_name = link["target"]
            data_dict[link_cid]["links"].append(link)
            if source_name not in unique_node_dict[link_cid]:
                data_dict[link_cid]["nodes"].append(source)
                unique_node_dict[link_cid].add(source_name)
            if target_name not in unique_node_dict[link_cid]:
                data_dict[link_cid]["nodes"].append(target)
                unique_node_dict[link_cid].add(target_name)
        networks: List[Network] = []
        for cid in range(n_networks):
            metadata = data_dict[cid]["metadata"]
            nodes = data_dict[cid]["nodes"]
            links = data_dict[cid]["links"]
            network_raw_data = {**metadata, "nodes": nodes, "links": links}
            networks.append(Network.load_json(raw_data=network_raw_data))
        return cls(networks)

    def combine_pvalues(self) -> pd.Series:
        """
        Combine pvalues of links in the network group using the Brown's Method

        Returns
        -------
        pvalues_combined
            The `pd.Series` containing the combined pvalues
        """
        pvalue_vectors = self.get_adjacency_vectors("pvalue")
        weight_vectors = self.get_adjacency_vectors("weight")
        pvalue_df: pd.DataFrame = pd.concat(pvalue_vectors, join="outer")
        weight_df: pd.DataFrame = pd.concat(weight_vectors, join="outer")
        # E[psi] = 2 * k
        k = pvalue_df.shape[1]
        expected_value = 2 * k
        # Var[psi] = 4*k + 2 * sum{i<j} (3.263 * corr_ij + 0.710 * corr_ij^2 + 0.027 * corr_ij^3)
        variance = 4 * k
        for i in range(1, k):
            for j in range(0, i - 1):
                x_i = weight_df.iloc[:, i].values
                x_j = weight_df.iloc[:, j].values
                corr_ij, _ = pearsonr(x_i, x_j)
                cov_ij_approx = (
                    3.263 * corr_ij + 0.710 * (corr_ij ** 2) + 0.027 * (corr_ij ** 3)
                )
                variance += 2 * cov_ij_approx
        # df = 2 * E[psi]^2 / var[psi]
        degrees_of_freedom = 2 * (expected_value ** 2) / variance
        # c = var[psi] / (2 * E[psi])
        correction_factor = variance / (2 * expected_value)
        link_ids = list(pvalue_df.index)
        pvalues_combined = pd.Series(data=np.zeros(len(link_ids)), index=link_ids)
        for row_id in list(pvalue_df.index):
            pvalues = pvalue_df[row_id, :].values
            chi_square = -2.0 * np.log(pvalues).sum() / correction_factor
            pvalues_combined[row_id] = chi2.sf(chi_square, df=degrees_of_freedom)
        return pvalues_combined
