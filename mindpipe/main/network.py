"""
    Module that defines the `Network` object and methods to read, write and manipulate it
"""

import json
from typing import Any, Dict, List, Optional, Set, FrozenSet, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from . import Lineage
from ..validation import (
    InteractionmatrixType,
    CorrelationmatrixType,
    PvaluematrixType,
    ObsmetaType,
    MetadataModel,
    ChildrenmapType,
    NodesModel,
    LinksModel,
    NetworkmetadataModel,
    ElistType,
)
from ..utils import JsonEncoder


class Network:
    """
        Class that represents a network object

        Parameters
        ----------
        interactions : pd.SparseDataFrame
            The `SparseDataFrame` containing the matrix of interactions
        metadata : dict
            The metadata for the whole network (general and experiment)
            Must contain 'host', 'condition', 'location', 'experimental_metadata', 'pubmed_id',
            'description', 'date', 'authors
        cmetadata : dict
            The computational metadata for the whole network
            Must contain information as to how the network was generated
        obs_metadata : pd.DataFrame
            The `DataFrame` containing taxonomy information for the nodes of the network
            If this contains an 'Abundance' column then it is incorporated into the network
        pvalues : pd.DataFrame, optional
            The `DataFrame` containing the matrix of pvalues
        children_map : dict, optional
            The dictionary that contains the mapping {obs_id => [children]}
        interaction_type : str, optional
            The type of interaction encoded by the edges of the network
            Default value is correlation
        interaction_threshold : float, optional
            The value to which the interactions (absolute value) are to be thresholded
            To disable thresholding based on interaction value then pass in 0.0
            Default value is 0.3
        pvalue_threshold : float, optional
            This is the `alpha` value for pvalue cutoff
            Default value is 0.05
        pvalue_correction : str, optional
            The method to use for multiple hypothesis correction
            Default value is 'fdr_bh'
            Set to None to turn off multiple hypothesis correction
            Use `Network.pcorr_methods` to get the list of supported methods
        directed : bool, optional
            True if network is directed
            Default value is False

        Attributes
        ----------
        nodes : List[Dict[str, Any]]
            The list of nodes in the network and their corresponding properties
        links : List[Dict[str, Any]]
            The list of links in the network and their corresponding properties
        filtered_links : List[Dict[str, Any]]
            The list of links in the network after applying thresholds
        metadata : Dict[str, Any]
            The metadata for the network
        graph : nx.Graph
            The networkx graph representation of the network

        Examples
        --------
        >>> network = Network.load()
    """

    def __init__(
        self,
        interactions: pd.SparseDataFrame,
        metadata: dict,
        cmetadata: dict,
        obs_metadata: pd.DataFrame,
        pvalues: Optional[pd.DataFrame] = None,
        children_map: Optional[dict] = None,
        interaction_type: str = "correlation",
        interaction_threshold: float = 0.3,
        pvalue_threshold: float = 0.05,
        pvalue_correction: Optional[str] = "fdr_bh",
        directed: bool = False,
    ) -> None:
        obsmeta_validator = ObsmetaType()
        obsmeta_validator.validate(obs_metadata)
        metadata_model = MetadataModel(metadata, strict=False)
        metadata_model.validate()
        if children_map:
            children_validator = ChildrenmapType()
            children_validator.validate(children_map)
        if interaction_type == "correlation":
            interaction_validator = CorrelationmatrixType()
        else:
            interaction_validator = InteractionmatrixType(symm=not directed)
        interaction_validator.validate(interactions)
        if pvalues is not None:
            self._verify_integrity(interactions, pvalues)
            pvalue_validator = PvaluematrixType(symm=directed)
            pvalue_validator.validate(pvalues)
            if pvalue_correction:
                corrected_pvalues = self._correct_pvalues(
                    pvalues, pvalue_correction, pvalue_threshold
                )
            else:
                corrected_pvalues = pvalues
            if "pvalue_threshold" not in cmetadata:
                cmetadata["pvalue_threshold"] = pvalue_threshold
            if "pvalue_correction" not in cmetadata:
                cmetadata["pvalue_correction"] = pvalue_correction
        else:
            corrected_pvalues = None
        if "interaction_threshold" not in cmetadata:
            cmetadata["interaction_threshold"] = interaction_threshold
        self.nodes, self.links, self.metadata = self._create_network(
            interactions,
            corrected_pvalues,
            obs_metadata,
            metadata,
            cmetadata,
            children_map,
            interaction_type,
            directed,
        )
        self.interaction_threshold = interaction_threshold
        self.pvalue_threshold = pvalue_threshold
        self._pvalue_flag = True if pvalues is not None else False

    def __repr__(self) -> str:
        n_nodes = len(self.nodes)
        n_links = len(self.links)
        directionality = self.metadata["directionality"]
        interaction_type = self.metadata["interaction_type"]
        string = (
            f"<Network nodes={n_nodes} links={n_links} "
            f"type={interaction_type} directionality={directionality}>"
        )
        return string

    @staticmethod
    def _verify_integrity(interactions: pd.DataFrame, pvalues: pd.DataFrame) -> None:
        """
            Verify whether the interactions and pvalue matrices match

            Parameters
            ----------
            interactions : pd.DataFrame
                The `DataFrame` containing the interaction matrix
            pvalues : pd.DataFrame
                The `DataFrame` containing the pvalue matrix
        """
        if any(interactions.index != pvalues.index) or any(
            interactions.columns != pvalues.columns
        ):
            raise ValueError(
                "Interaction and pvalue matrices do not have matching indices"
            )

    @property
    def pcorr_methods(self) -> List[str]:
        """
            Returns list supported pvalue correction methods
        """
        methods = [
            "bonferroni",
            "sidak",
            "holm-sidak",
            "holm",
            "simes-hochberg",
            "hommel",
            "fdr_bh",
            "fdr_by",
            "fdr_tsbh",
            "fdr_tsbky",
        ]
        return methods

    def _correct_pvalues(
        self, pvalues: pd.DataFrame, method: str, pvalue_threshold: float
    ) -> pd.DataFrame:
        """
            Correct pvalues using 'method'

            Parameters
            ----------
            pvalues : pd.DataFrame
                Raw uncorrected pvalues
            method : str
                Method to be used to correct the pvalues.
                Use `Network.pcorr_methods` to get the list of supported methods
            pvalue_threshold : float
                The value of alpha (FWER) to be used for the correction

            Returns
            -------
            pd.DataFrame
                DataFrame containing corrected pvalues
        """
        if method not in self.pcorr_methods:
            raise ValueError(
                f"Method {method} not supported. Must be one of {self.pcorr_methods}"
            )
        flat_pvalues = pvalues.values.flatten()
        reject, pvals_correct, *_ = multipletests(
            flat_pvalues, alpha=pvalue_threshold, method=method
        )
        pval_correct_df = pd.DataFrame(
            data=pvals_correct.reshape(pvalues.shape),
            index=pvalues.index,
            columns=pvalues.columns,
        ).to_sparse()
        return pval_correct_df

    @staticmethod
    def _create_network(
        interactions: pd.SparseDataFrame,
        pvalues: Optional[pd.DataFrame],
        obs_metadata: pd.DataFrame,
        emetadata: dict,
        cmetadata: dict,
        children_map: Optional[dict],
        interaction_type: str,
        directed: bool,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
        """
            Create network from interaction matrix, pvalue matrix, metadata dictionary,
            lineage table and children mapping

            Parameters
            ----------
            interactions : pd.SparseDataFrame
                The `SparseDataFrame` containing the matrix of interactions
            pvalues : Optional[pd.DataFrame]
                The `DataFrame` containing the *corrected* pvalues
            obs_metadata : pd.DataFrame
                The `DataFrame` containing taxonomy information for the nodes of the network
            emetadata : dict
                The dictionary of general and experimental metadata
            cmetadata : dict
                The dictionary of computational metadata
            children_map : dict
                The dictionary that contains the mapping {obs_id => [children]}
            interaction_type : str
                The type of interaction encoded by the edges of the network
                The
            directed : bool
                Flag to determine whether the network is directed or not

            Returns
            -------
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]
                Nodes, Links, Metadata
        """
        directionality = "directed" if directed else "undirected"
        metadata = {
            **emetadata,
            "computational_metadata": cmetadata,
            "interaction_type": interaction_type,
            "directionality": directionality,
        }
        nodes: List[Dict[str, Any]] = []
        abundance_flag = "Abundance" in obs_metadata.columns
        for node in interactions.index:
            if abundance_flag:
                lineage = Lineage(**obs_metadata.drop("Abundance").loc[node].to_dict())
                abundance = obs_metadata.loc[node].Abundance
            else:
                if node not in obs_metadata.index:
                    lineage = Lineage(Kingdom="Bacteria")
                else:
                    lineage = Lineage(**obs_metadata.loc[node].to_dict())
                abundance = None
            if children_map:
                children = children_map.get(node, [])
            else:
                children = []
            sup_lineage = lineage.get_superset(lineage.taxid[0])
            nodes.append(
                {
                    "id": node,
                    "lineage": sup_lineage.to_str(
                        style="gg", level=sup_lineage.name[0]
                    ),
                    "name": sup_lineage.name[1],
                    "taxid": sup_lineage.taxid[1],
                    "taxlevel": sup_lineage.name[0],
                    "abundance": abundance,
                    "children": children,
                }
            )
        link_set: Set[FrozenSet[str]] = set()
        links: List[Dict[str, Any]] = []
        stack = interactions.stack()
        for nnz_ind in stack.nonzero()[0]:
            source, target = stack.index[nnz_ind]
            if source == target:
                continue
            if not directed and frozenset([source, target]) in link_set:
                continue
            weight = interactions.at[source, target]
            pvalue = pvalues.at[source, target] if pvalues is not None else None
            links.append(
                {"source": source, "target": target, "weight": weight, "pvalue": pvalue}
            )
            if not directed:
                link_set.add(frozenset([source, target]))
        # TODO: validate=True
        nodes_model = NodesModel({"nodes": nodes}, strict=False)
        nodes_model.validate()
        links_model = LinksModel({"links": links}, strict=False)
        links_model.validate()
        networkmetadata_model = NetworkmetadataModel(metadata, strict=False)
        networkmetadata_model.validate()
        return nodes, links, metadata

    @property
    def filtered_links(self) -> List[Dict[str, Any]]:
        """
            The links of the network after applying filtering

            Returns
            -------
            List[Dict[str, Any]]
                The list of links in the network after applying a threshold
        """
        interaction_threshold = abs(self.interaction_threshold)
        interaction_filter = lambda x: abs(x["weight"]) >= interaction_threshold
        pvalue_filter = lambda x: x["pvalue"] <= self.pvalue_threshold
        if self._pvalue_flag:
            filter_fun = lambda x: interaction_filter(x) and pvalue_filter(x)
        else:
            filter_fun = interaction_filter
        links_thres = list(filter(filter_fun, self.links))
        return links_thres

    @classmethod
    def load_data(
        cls,
        interaction_file: str,
        meta_file: str,
        cmeta_file: str,
        obsmeta_file: str,
        pvalue_file: Optional[str] = None,
        children_file: Optional[str] = None,
        interaction_type: str = "correlation",
        interaction_threshold: float = 0.3,
        pvalue_threshold: float = 0.05,
        pvalue_correction: Optional[str] = "fdr_bh",
        directed: bool = False,
    ) -> "Network":
        """
            Create a `Network` object from files (interaction tables and other metadata)

            Parameters
            ----------
            interaction_file : str
                The `tsv` file containing the matrix of interactions
            meta_file : str
                The `json` file containing the metadata for the whole network (general and experiment)
            cmeta_file : str
                The `json` file containings the computational metadata for the whole network
            obsmeta_file : str
                The `csv` file containing taxonomy information for the nodes of the network
            pvalue_file : str, optional
                The `tsv` file containing the matrix of pvalues
                Default is None
            children_file : str, optional
                The `json` file containing the mapping between observations and their children
            interaction_type : str, optional
                The type of interaction encoded by the edges of the network
                Default value is correlation
            interaction_threshold : float, optional
                The value to which the interactions (absolute value) are to be thresholded
                To disable thresholding based on interaction value then pass in 0.0
                Default value is 0.3
            pvalue_threshold : float, optional
                This is the `alpha` value for pvalue cutoff
                Default value is 0.05
            pvalue_correction : str, optional
                The method to use for multiple hypothesis correction
                Default value is 'fdr_bh'
                Set to None to turn off multiple hypothesis correction
                Use `Network.pcorr_methods` to get the list of supported methods
            directed : bool
                True if network is directed
                Default value is False

            Returns
            -------
            Network
                The instance of the `Network` class
        """
        interactions = pd.read_table(interaction_file, index_col=0).to_sparse(
            fill_value=0.0
        )
        with open(meta_file, "r") as fid:
            metadata = json.load(fid)
        with open(cmeta_file, "r") as fid:
            cmetadata = json.load(fid)
        if pvalue_file:
            extra_compdata = {
                "interaction_threshold": interaction_threshold,
                "pvalue_threshold": pvalue_threshold,
                "pvalue_correction": pvalue_correction,
            }
        else:
            extra_compdata = {"interaction_threshold": interaction_threshold}
        cmetadata = {**cmetadata, **extra_compdata}
        obs_metadata = pd.read_csv(obsmeta_file, index_col=0, na_filter=False)
        if pvalue_file is not None:
            pvalues = pd.read_table(pvalue_file, index_col=0)
        else:
            pvalues = None
        if children_file is not None:
            with open(children_file, "r") as fid:
                children_map = json.load(fid)
        else:
            children_map = None
        network = cls(
            interactions,
            metadata,
            cmetadata,
            obs_metadata,
            pvalues,
            children_map,
            interaction_type,
            interaction_threshold,
            pvalue_threshold,
            pvalue_correction,
            directed,
        )
        return network

    @property
    def graph(self) -> nx.Graph:
        """ Networkx representation of the network """
        if self.metadata["directionality"] == "directed":
            graph = nx.DiGraph(**self.metadata)
        else:
            graph = nx.Graph(**self.metadata)
        for node in self.nodes:
            graph.add_node(node["id"], **node)
        for link in self.links:
            graph.add_edge(link["source"], link["target"], **link)
        return graph

    def json(self, threshold: bool = True) -> str:
        """ Network as a JSON string """
        nodes = {"nodes": self.nodes}
        if threshold:
            links = {"links": self.filtered_links}
        else:
            links = {"links": self.links}
        metadata = self.metadata
        network = {**metadata, **nodes, **links}
        return json.dumps(network, indent=2, sort_keys=True, cls=JsonEncoder)

    def write(self, fpath: str, threshold: bool = True) -> None:
        """
            Write network to file as JSON

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
    def load_json(cls, fpath: str) -> "Network":
        """
            Create a `Network` object from a network `JSON` file

            Parameters
            ----------
            fpath : str
                The path to the network `JSON` file

            Returns
            -------
            Network
                The instance of the `Network` class
        """
        with open(fpath, "r") as fid:
            raw_data = json.load(fid)
        # Validation
        nodes_model = NodesModel({"nodes": raw_data["nodes"]}, strict=False)
        nodes_model.validate()
        links_model = LinksModel({"links": raw_data["links"]}, strict=False)
        links_model.validate()
        non_meta_keys = ["nodes", "links"]
        metadata = {k: v for k, v in raw_data.items() if k not in non_meta_keys}
        networkmetadata_model = NetworkmetadataModel(metadata, strict=False)
        networkmetadata_model.validate()
        # Variable assignment
        cmetadata = raw_data["computational_metadata"]
        interaction_type = raw_data["interaction_type"]
        interaction_threshold = cmetadata["interaction_threshold"]
        pvalue_threshold = cmetadata["pvalue_threshold"]
        pvalue_correction = None
        directed = True if raw_data["directionality"] == "directed" else False
        index: List[str] = []
        lineages: List[dict] = []
        children_map: Dict[str, List[str]] = {}
        for node in raw_data["nodes"]:
            index.append(node["id"])
            lineage = Lineage.from_str(node["lineage"]).to_dict("Species")
            children_map[node["id"]] = node["children"]
            abundance = node.get("abundance")
            if abundance is not None:
                lineages.append({**lineage, **dict(abundance=abundance)})
            else:
                lineages.append(lineage)
        obs_metadata = pd.DataFrame(lineages, index=index)
        mat_shape = (len(index), len(index))
        dense_interactions = pd.DataFrame(
            data=np.zeros(mat_shape), index=index, columns=index
        )
        pvalue_flag = True if raw_data["links"][0]["pvalue"] is not None else False
        if pvalue_flag:
            pvalues = pd.DataFrame(data=np.zeros(mat_shape), index=index, columns=index)
        else:
            pvalues = None
        for link in raw_data["links"]:
            source, target = link["source"], link["target"]
            dense_interactions.at[source, target] = link["weight"]
            if not directed:
                dense_interactions.loc[target, source] = link["weight"]
            if pvalue_flag:
                pvalues.at[source, target] = link["pvalue"]
                if not directed:
                    pvalues.loc[target, source] = link["pvalue"]
        interactions = dense_interactions.to_sparse(fill_value=0.0)
        network = cls(
            interactions,
            metadata,
            cmetadata,
            obs_metadata,
            pvalues,
            children_map,
            interaction_type,
            interaction_threshold,
            pvalue_threshold,
            pvalue_correction,
            directed,
        )
        return network

    @classmethod
    def load_elist(
        cls,
        elist_file: str,
        meta_file: str,
        cmeta_file: str,
        obsmeta_file: str,
        children_file: Optional[str] = None,
        interaction_type: str = "correlation",
        interaction_threshold: float = 0.3,
        pvalue_threshold: float = 0.05,
        pvalue_correction: Optional[str] = "fdr_bh",
        directed: bool = False,
    ) -> "Network":
        """
            Create `Network` instance from an edge list and associated metadata

            Parameters
            ----------
            elist_file : str
                The csv file containing the list of edges and their associated metadata
            meta_file : dict
                The file containing metadata for the whole network (general and experiment)
                Must contain 'host', 'condition', 'location', 'experimental_metadata', 'pubmed_id',
                'description', 'date', 'authors'
            cmeta_file : dict
                The computational metadata for the whole network
                Must contain information as to how the network was generated
            obsmeta_file : str
                The csv file contanining taxonomy information for the nodes of the network
                If this contains an 'Abundance' column then it is incorporated into the network
            children_file : str, optional
                The json file that describes the mapping between {obs_id => [children]}
            interaction_type : str, optional
                The type of interaction encoded by the edges of the network
                Default value is correlation
            interaction_threshold : float, optional
                The value to which the interactions (absolute value) are to be thresholded
                To disable thresholding based on interaction value then pass in 0.0
                Default value is 0.3
            pvalue_threshold : float, optional
                This is the `alpha` value for pvalue cutoff
                Default value is 0.05
            pvalue_correction : str, optional
                The method to use for multiple hypothesis correction
                Default value is 'fdr_bh'
                Set to None to turn off multiple hypothesis correction
            directed : bool, optional
                True if network is directed
                Default value is False

            Returns
            -------
            Network
                The instance of the `Network` class
        """
        elist = pd.read_csv(elist_file, na_filter=False)
        elist_type = ElistType()
        elist_type.validate(elist)
        index = list(set([*elist["source"], *elist["target"]]))
        mat_shape = len(index), len(index)
        interactions = pd.DataFrame(
            data=np.zeros(mat_shape), index=index, columns=index
        )
        pvalue_flag = True if "pvalue" in elist.columns else False
        if pvalue_flag:
            pvalues = pd.DataFrame(data=np.zeros(mat_shape), index=index, columns=index)
        else:
            pvalues = None
        for entry in elist.to_dict("records"):
            source, target, weight = entry["source"], entry["target"], entry["weight"]
            interactions.at[source, target] = weight
            if not directed:
                interactions.loc[target, source] = weight
            if pvalue_flag:
                pvalues.at[source, target] = entry["pvalue"]
                if not directed:
                    pvalues.loc[target, source] = entry["pvalue"]
        with open(meta_file, "r") as fid:
            metadata = json.load(fid)
        with open(cmeta_file, "r") as fid:
            cmetadata = json.load(fid)
        if pvalue_flag:
            extra_compdata = {
                "interaction_threshold": interaction_threshold,
                "pvalue_threshold": pvalue_threshold,
                "pvalue_correction": pvalue_correction,
            }
        else:
            extra_compdata = {"interaction_threshold": interaction_threshold}
        cmetadata = {**cmetadata, **extra_compdata}
        obs_metadata = pd.read_csv(obsmeta_file, index_col=0, na_filter=False)
        if children_file is not None:
            with open(children_file, "r") as fid:
                children_map = json.load(fid)
        else:
            children_map = None
        pvalue_correction = None  # To prevent re-correction of pvalues
        network = cls(
            interactions,
            metadata,
            cmetadata,
            obs_metadata,
            pvalues,
            children_map,
            interaction_type,
            interaction_threshold,
            pvalue_threshold,
            pvalue_correction,
            directed,
        )
        return network
