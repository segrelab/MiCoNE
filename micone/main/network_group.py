"""
    Module that defines the `NetworkGroup` object and methods to read, write and manipulate it
"""

from collections import defaultdict
from collections.abc import Collection
import pathlib
from itertools import product
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

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
        # dict(cid => dict(id_old => id_new))
        self.nodeid_map: Dict[int, Dict[str, str]] = dict()
        # dict(s_new-t_new => List[Tuple[cid, s_old-t_old], ...])
        self.linkid_revmap: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
        self._networks = tuple(networks)
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
        """Combine nodes of individual networks into a single list"""
        nodes: DType = []
        node_hash: Dict[int, int] = dict()  # taxid => nodes.index
        if len(all_nodes) == 1:
            return all_nodes[0]
        for cid, network_nodes in all_nodes.items():
            self.nodeid_map[cid] = dict()
            for network_node in network_nodes:
                if network_node["taxid"] not in node_hash:
                    id_ = len(nodes)
                    id_old = network_node["id"]
                    id_new = f"id{id_}"
                    nodes.append(
                        {
                            **network_node,
                            **{"id": id_new, "children": [], "abundance": None},
                        }
                    )
                    node_hash[network_node["taxid"]] = id_
                    self.nodeid_map[cid][id_old] = id_new
                else:
                    id_old = network_node["id"]
                    ind = node_hash[network_node["taxid"]]
                    id_new = nodes[ind]["id"]
                    self.nodeid_map[cid][id_old] = id_new
        return nodes

    def _combine_links(
        self, all_links: Dict[int, DType], inplace: bool = True
    ) -> DType:
        """Combine links of individual networks into a single list"""
        links = []
        if len(all_links) == 1:
            for link in all_links[0]:
                source, target = link["source"], link["target"]
                if inplace:
                    self.linkid_revmap[f"{source}-{target}"].append(
                        (0, f"{source}-{target}")
                    )
                links.append({**link, "context_index": 0})
            return links
        for cid, network_links in all_links.items():
            for link in network_links:
                source, target = link["source"], link["target"]
                new_source = self.nodeid_map[cid][source]
                new_target = self.nodeid_map[cid][target]
                if inplace:
                    self.linkid_revmap[f"{new_source}-{new_target}"].append(
                        (cid, f"{source}-{target}")
                    )
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
        """The list of nodes in the `NetworkGroup` and their corresponding properties"""
        return [data for _, data in self.graph.nodes(data=True)]

    @property
    def links(self) -> DType:
        """The list of links in the `NetworkGroup` and their corresponding properties"""
        return [data for _, _, data in self.graph.edges(data=True)]

    @property
    def contexts(self) -> DType:
        """The contexts for the group of networks"""
        return self.graph.graph["contexts"]

    def get_adjacency_vectors(self, key: str) -> pd.DataFrame:
        """
        Returns the adjacency matrix for each context as a `pd.DataFrame`

        Parameters
        ----------
        key : str
            The `edge` property to be used to contruct the vectors

        Returns
        -------
        pd.DataFrame:
            The DataFrame containing adjacency vectors as columns
        """
        ids = list(self.graph.nodes)
        size = len(ids) * len(ids)
        # NOTE: This will consider id1-id2 and id2-id1 as different (even for undirected)
        index = [f"{id1}-{id2}" for id1, id2 in product(ids, repeat=2)]
        n_contexts = len(self)
        adj_vector_df: pd.DataFrame = pd.concat(
            [
                pd.Series(np.zeros((size), dtype=float), index=index)
                for _ in range(n_contexts)
            ],
            join="outer",
            axis=1,
        )
        graph = self.graph
        # NOTE: networkx automatically handles directionality (source -> target) here
        for source, target, data in graph.edges(data=True, keys=False):
            cid = data["context_index"]
            id_ = f"{source}-{target}"
            adj_vector_df.loc[id_, cid] = data[key]
        return adj_vector_df

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
        for context in self.graph.graph["contexts"]:
            context["interaction_threshold"] = interaction_threshold
            context["pvalue_threshold"] = pvalue_threshold
        for network in self._networks:
            network.interaction_threshold = interaction_threshold
            network.pvalue_threshold = pvalue_threshold

    def _filter_links(self, pvalue_filter: bool, interaction_filter: bool) -> DType:
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
            filtered_links_dict[cid] = network._filter_links(
                pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
            )
        merged_filtered_links = self._combine_links(filtered_links_dict, inplace=False)
        return merged_filtered_links

    def filter(self, pvalue_filter: bool, interaction_filter: bool) -> "NetworkGroup":
        """Filter network using pvalue and interaction thresholds

        Parameters
        ----------
        pvalue_filter : bool
            If `True` will use `pvalue_threshold` for filtering
        interaction_filter : bool
            If `True` will use `interaction_threshold` for filtering

        Returns
        -------
        "NetworkGroup"
            The filtered `NetworkGroup` object
        """
        nodes = {"nodes": self.nodes}
        links = {
            "links": self._filter_links(
                pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
            )
        }
        contexts = {"contexts": self.contexts}
        network_data = {**contexts, **nodes, **links}
        new_network = NetworkGroup.load_json(raw_data=network_data)
        return new_network

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
        links = self._filter_links(
            pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
        )
        contexts = self.contexts
        network = {"contexts": contexts, "nodes": nodes, "links": links}
        return simplejson.dumps(network, indent=2, sort_keys=True, ignore_nan=True)

    def write(
        self,
        fpath: str,
        pvalue_filter: bool = False,
        interaction_filter: bool = False,
        split_files: bool = False,
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
        split_files : bool
            If True will write networks into separate files
            Default value is False
        """
        if not split_files:
            with open(fpath, "w") as fid:
                fid.write(
                    self.json(
                        pvalue_filter=pvalue_filter,
                        interaction_filter=interaction_filter,
                    )
                )
        else:
            for cid, network in enumerate(self._networks):
                path = pathlib.Path(fpath)
                fname = f"{path.parent}/{cid}_{path.stem}{path.suffix}"
                network.write(
                    fname,
                    pvalue_filter=pvalue_filter,
                    interaction_filter=interaction_filter,
                )

    @classmethod
    def load_json(
        cls, fpath: Optional[str] = None, raw_data: Optional[dict] = None
    ) -> "NetworkGroup":
        """
        Create a `NetworkGroup` object from network `JSON` file
        Either fpath or raw_data must be specified

        Parameters
        ----------
        fpath : str, optional
            The path to the network `JSON` file
        raw_data : dict, optional
            The raw data stored in the network `JSON` file

        Returns
        -------
        NetworkGroup
            The instance of the `NetworkGroup` class
        """
        if not raw_data and not fpath:
            raise ValueError("Either fpath or raw_data must be specified")
        if not raw_data and fpath:
            with open(fpath, "r") as fid:
                data = simplejson.load(fid)
        else:
            data: dict = raw_data
        n_networks = len(data["contexts"])
        all_node_dict = {n["id"]: n for n in data["nodes"]}
        data_dict: Dict[int, dict] = {
            n: {"nodes": [], "links": [], "metadata": {}} for n in range(n_networks)
        }
        unique_node_dict: Dict[int, dict] = {n: set() for n in range(n_networks)}
        for cid in range(n_networks):
            data_dict[cid]["metadata"] = {**data["contexts"][cid]}
        for link in data["links"]:
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
            network_data = {**metadata, "nodes": nodes, "links": links}
            networks.append(Network.load_json(raw_data=network_data))
        return cls(networks)

    def get_consensus_network(
        self, cids: List[str], method: str = "simple_voting", parameter: float = 0.0
    ) -> "NetworkGroup":
        """
        Get consensus network for the network defined by the `cids`

        Parameters:
        -----------
        cids : List[str]
            The list of context ids that are to be used in the merger
        method : str, {"simple_voting", "scaled_sum"}
            Default value is simple_voting
        parameter : float
            Default value is 0.0 (which is the union of all the links)

        Returns
        -------
        consensus_network
            The `NetworkGroup` that represents the consensus network
        """

        # Method 1: Simple voting method
        def simple_voting(weights: pd.DataFrame, parameter: float) -> List[str]:
            """Perform a simple voting consensus"""
            size = weights.shape[1]  # no. of networks
            num_req_edges = np.floor(parameter * size)
            num_actual_edges = weights.astype(bool).sum(axis=1)
            indices_removal = weights.index[num_actual_edges < num_req_edges]
            return list(indices_removal)

        # Method 2: Scaled sum method
        def scaled_sum(weights: pd.DataFrame, parameter: float) -> List[str]:
            """Peform a scaled sum consensus"""
            size = weights.shape[1]  # no. of networks
            weights_scaled = weights.apply(lambda x: x / (np.abs(x).max()))
            parameter_scaled = (size - 1) * parameter
            indices_removal = weights.index[
                weights_scaled.sum(axis=1) < parameter_scaled
            ]
            return list(indices_removal)

        # Step1: Filter by "cids" and make copies of graphs
        graphs = []
        for cid, network in enumerate(self._networks):
            if cid in cids:
                graphs.append(network.graph.copy())
        weights: pd.DataFrame = self.get_adjacency_vectors("weight")[cids]
        # Filling with dummy values
        weights.fillna(0.0, inplace=True)  # dummy weights = 0

        # Step 2: Apply voting method to each multiedge
        # indices_removal has {new_id_source}-{new_id_target}
        if method == "simple_voting":
            indices_removal = simple_voting(weights, parameter)
        elif method == "scaled_sum":
            indices_removal = scaled_sum(weights, parameter)
        else:
            raise ValueError("Only methods supported are simple_voting and scaled_sum")

        # Step 3: Use indices_removal on the networks
        graph_dict = dict(enumerate(graphs))
        for ind in indices_removal:
            for cid, ind_old in self.linkid_revmap[ind]:
                source_old, target_old = ind_old.split("-")
                graph_dict[cid].remove_edge(source_old, target_old)
        new_networks = [Network.load_graph(graph) for graph in graph_dict.values()]

        # Step 4: Return NetworkGroup object
        return NetworkGroup(new_networks)

    def combine_pvalues(self, cids: List[int]) -> "NetworkGroup":
        """
        Combine pvalues of links in the `cids` using Brown's p-value merging method

        Parameters:
        -----------
        cids : List[int]
            The list of context ids that are to be used in the merger

        Returns
        -------
        merged_network
            The `NetworkGroup` that contains the merged pvalues
        """

        # Step 1: Obtain the pvalues and weights
        weight_df: pd.DataFrame = self.get_adjacency_vectors("weight")[cids]
        pvalue_df: pd.DataFrame = self.get_adjacency_vectors("pvalue")[cids]

        # Filling with dummy values
        weight_df.fillna(0.0, inplace=True)  # dummy weights = 0
        pvalue_df.fillna(1.0, inplace=True)  # dummy pvalues = 1
        eps = np.finfo(np.float).eps
        pvalue_df.replace(0.0, eps, inplace=True)  # to prevent log(0)

        # Step 2: Calculate the combined pvalues using Browns method
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
        link_ids = pvalue_df.index
        chi_square = pvalue_df.apply(
            lambda x: -2.0 * np.log(x).sum() / correction_factor, axis=1
        )
        pvalues_combined = pd.Series(
            data=chi2.sf(chi_square, df=degrees_of_freedom), index=link_ids
        )

        # Step 3: Create new networks
        graphs = []
        for cid, network in enumerate(self._networks):
            if cid in cids:
                graphs.append(network.graph.copy())
        graph_dict = dict(enumerate(graphs))
        for ind in pvalues_combined.index:
            for cid, ind_old in self.linkid_revmap[ind]:
                source_old, target_old = ind_old.split("-")
                graph_dict[cid].edges[source_old, target_old][
                    "pvalue"
                ] = pvalues_combined[ind]
        new_networks = [Network.load_graph(graph) for graph in graphs]

        # Step 4: Return NetworkGroup object
        return NetworkGroup(new_networks)
