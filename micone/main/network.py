"""
    Module that defines the `Network` object and methods to read, write and manipulate it
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from warnings import warn

import networkx as nx
import numpy as np
import pandas as pd
import simplejson
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


DType = List[Dict[str, Any]]
LinkDType = Tuple[str, str, Dict[str, float]]


class Network:
    """
    Class that represents a network object

    Parameters
    ----------
    nodes : List[str]
        The list of nodes in the network
    links : List[LinkDType]
        The list of links in the network
        Each link is a dict and must contain: 'source', 'target', 'weight', 'pvalue' as keys
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
    graph : Union[nx.Graph, nx.DiGraph]
        The networkx graph representation of the network
    nodes : DType
        The list of nodes in the network and their corresponding properties
    links : DType
        The list of links in the network and their corresponding properties
    metadata : Dict[str, Any]
        The metadata for the network

    Examples
    --------
    >>> network = Network.load_data()
    """

    def __init__(
        self,
        nodes: List[str],
        links: List[LinkDType],
        metadata: dict,
        cmetadata: dict,
        obs_metadata: pd.DataFrame,
        children_map: Optional[dict] = None,
        interaction_type: str = "correlation",
        interaction_threshold: float = 0.3,
        pvalue_threshold: float = 0.05,
        pvalue_correction: Optional[str] = "fdr_bh",
        directed: bool = False,
    ) -> None:
        self.interaction_threshold = interaction_threshold
        self.pvalue_threshold = pvalue_threshold
        obsmeta_validator = ObsmetaType()
        obsmeta_validator.validate(obs_metadata)
        metadata_model = MetadataModel(metadata, strict=False)
        metadata_model.validate()
        if children_map:
            children_validator = ChildrenmapType()
            children_validator.validate(children_map)
        pvalues = np.array([link[2]["pvalue"] for link in links])
        if pvalue_correction:
            corrected_pvalues = self._correct_pvalues(
                pvalues, pvalue_correction, pvalue_threshold
            )
        else:
            corrected_pvalues = pvalues
        corrected_links: List[LinkDType] = []
        for i, link in enumerate(links):
            source, target = link[0], link[1]
            corrected_links.append(
                (source, target, {**link[2], "pvalue": corrected_pvalues[i]})
            )
        if "pvalue_threshold" not in cmetadata:
            cmetadata["pvalue_threshold"] = pvalue_threshold
        if "pvalue_correction" not in cmetadata:
            cmetadata["pvalue_correction"] = pvalue_correction
        if "interaction_threshold" not in cmetadata:
            cmetadata["interaction_threshold"] = interaction_threshold
        self.graph = self._create_graph(
            nodes,
            corrected_links,
            metadata,
            cmetadata,
            obs_metadata,
            children_map,
            interaction_type,
            directed,
        )
        nodes_model = NodesModel({"nodes": self.nodes}, strict=False)
        nodes_model.validate()
        links_model = LinksModel({"links": self.links}, strict=False)
        links_model.validate()
        networkmetadata_model = NetworkmetadataModel(self.metadata, strict=False)
        networkmetadata_model.validate()

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
        self, pvalues: np.array, method: str, pvalue_threshold: float
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
        _, pvals_correct, *_ = multipletests(
            pvalues, alpha=pvalue_threshold, method=method
        )
        return pvals_correct

    @staticmethod
    def _create_graph(
        nodes: List[str],
        links: List[LinkDType],
        emetadata: dict,
        cmetadata: dict,
        obs_metadata: pd.DataFrame,
        children_map: Optional[dict],
        interaction_type: str,
        directed: bool,
    ) -> Union[nx.Graph, nx.DiGraph]:
        """
        Create network from interaction matrix, pvalue matrix, metadata dictionary,
        lineage table and children mapping

        Parameters
        ----------
        nodes : List[str]
            The list of nodes in the network
        links : List[LinkDType]
            The list of links in the network
        emetadata : dict
            The dictionary of general and experimental metadata
        cmetadata : dict
            The dictionary of computational metadata
        obs_metadata : pd.DataFrame
            The `DataFrame` containing taxonomy information for the nodes of the network
        children_map : dict
            The dictionary that contains the mapping {obs_id => [children]}
        interaction_type : str
            The type of interaction encoded by the edges of the network
        directed : bool
            Flag to determine whether the network is directed or not

        Returns
        -------
        Union[nx.Graph, nx.DiGraph]
            The networkx graph of the network
        """
        directionality = "directed" if directed else "undirected"
        metadata = {
            **emetadata,
            "computational_metadata": cmetadata,
            "interaction_type": interaction_type,
            "directionality": directionality,
        }
        if directed:
            graph = nx.DiGraph(**metadata)
        else:
            graph = nx.Graph(**metadata)
        abundance_flag = "Abundance" in obs_metadata.columns
        for node in nodes:
            if abundance_flag:
                lineage = Lineage(
                    **obs_metadata.drop("Abundance", axis=1).loc[node].to_dict()
                )
                abundance = obs_metadata.loc[node].Abundance
            else:
                if node not in obs_metadata.index:
                    lineage = Lineage(Kingdom="Bacteria")
                    warn(
                        UserWarning(
                            f"{node} not found in obs_metadata. Assigning lineage as Bacteria"
                        )
                    )
                else:
                    lineage = Lineage(**obs_metadata.loc[node].to_dict())
                abundance = None
            if children_map:
                children = children_map.get(node, [])
            else:
                children = []
            sup_lineage = lineage.get_superset(lineage.taxid[0])
            graph.add_node(
                node,
                id=node,
                lineage=sup_lineage.to_str(style="gg", level=sup_lineage.name[0]),
                name=sup_lineage.name[1],
                taxid=sup_lineage.taxid[1],
                taxlevel=sup_lineage.name[0],
                abundance=abundance,
                children=children,
            )
        for link in links:
            source, target = link[0], link[1]
            # NOTE: Self-loops are not allowed
            if source == target:
                continue
            weight, pvalue = link[2]["weight"], link[2]["pvalue"]
            graph.add_edge(
                source,
                target,
                source=source,
                target=target,
                weight=weight,
                pvalue=pvalue,
            )
        return graph

    @property
    def nodes(self) -> DType:
        """The list of nodes in the network and their corresponding properties"""
        return [data for _, data in self.graph.nodes(data=True)]

    @property
    def links(self) -> DType:
        """The list of links in the network and their corresponding properties"""
        return [data for _, _, data in self.graph.edges(data=True)]

    @property
    def metadata(self) -> Dict[str, Any]:
        """The metadata for the network"""
        return self.graph.graph

    def get_adjacency_table(self, key: str) -> pd.DataFrame:
        """
        Returns the adjacency table representation for the requested `key`
        This method does not support `Graph`

        Parameters
        ----------
        key : str
            The `edge` property to be used to construct the table

        Returns
        -------
        pd.DataFrame:
            The adjacency table
        """
        ids = list(self.nodes)
        size = len(ids)
        adj_table = pd.DataFrame(
            data=np.zeros((size, size), dtype=float), index=ids, columns=ids
        )
        graph = self.graph
        for source_id, target_id, data in graph.edges(data=True):
            adj_table[source_id][target_id] = data[key]
            if not self.graph.is_directed():
                adj_table[target_id][source_id] = data[key]
        return adj_table

    def _filter_links(self, pvalue_filter: bool, interaction_filter: bool) -> DType:
        """
        The links of the network after applying filtering

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
        interaction_threshold = abs(self.interaction_threshold)
        interaction_func = lambda x: abs(x["weight"]) >= interaction_threshold
        pvalues = [l["pvalue"] for l in self.links]
        no_pvalues = np.isnan(pvalues).all()
        if no_pvalues:
            pvalue_func = lambda _: True
        else:
            pvalue_func = lambda x: x["pvalue"] <= self.pvalue_threshold
        if pvalue_filter and interaction_filter:
            filter_func = lambda x: interaction_func(x) and pvalue_func(x)
        elif interaction_filter:
            filter_func = interaction_func
        elif pvalue_filter:
            filter_func = pvalue_func
        else:
            return self.links
        links_thres = list(filter(filter_func, self.links))
        return links_thres

    def filter(self, pvalue_filter: bool, interaction_filter: bool) -> "Network":
        """Filter network using pvalue and interaction thresholds

        Parameters
        ----------
        pvalue_filter : bool
            If `True` will use `pvalue_threshold` for filtering
        interaction_filter : bool
            If `True` will use `interaction_threshold` for filtering

        Returns
        -------
        "Network"
            The filtered `Network` object
        """
        nodes = {"nodes": self.nodes}
        links = {
            "links": self._filter_links(
                pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
            )
        }
        metadata = self.metadata
        network_data = {**metadata, **nodes, **links}
        new_network = Network.load_json(raw_data=network_data)
        return new_network

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
        # Load and validate interaction matrix
        interactions = pd.read_table(interaction_file, index_col=0)
        if interaction_type == "correlation":
            interaction_validator = CorrelationmatrixType()
        else:
            interaction_validator = InteractionmatrixType(symm=not directed)
        interaction_validator.validate(interactions)
        # Load and validate pvalue matrix
        if pvalue_file is not None:
            pvalues = pd.read_table(pvalue_file, index_col=0)
            cls._verify_integrity(interactions, pvalues)
            pvalue_validator = PvaluematrixType(symm=directed)
            pvalue_validator.validate(pvalues)
        else:
            pvalues = None
        # If undirected convert to upper triangular matrix
        if directed:
            interaction_mat = interactions.values
        else:
            interaction_mat = np.triu(interactions.values)
        row_inds, col_inds = interaction_mat.nonzero()
        # Calculate nodes and links
        nodes = list(interactions.index)
        links: List[LinkDType] = []
        for rind, cind in zip(row_inds, col_inds):
            links.append(
                (
                    interactions.index[rind],
                    interactions.columns[cind],
                    {
                        "weight": interactions.iloc[rind, cind],
                        "pvalue": pvalues.iloc[rind, cind] if pvalue_file else np.nan,
                    },
                )
            )
        # Load metadata
        with open(meta_file, "r") as fid:
            metadata = simplejson.load(fid)
        with open(cmeta_file, "r") as fid:
            cmetadata = simplejson.load(fid)
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
        if children_file is not None:
            with open(children_file, "r") as fid:
                children_map = simplejson.load(fid)
        else:
            children_map = None
        network = cls(
            nodes,
            links,
            metadata,
            cmetadata,
            obs_metadata,
            children_map,
            interaction_type,
            interaction_threshold,
            pvalue_threshold,
            pvalue_correction,
            directed,
        )
        return network

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
        nodes = {"nodes": self.nodes}
        links = {
            "links": self._filter_links(
                pvalue_filter=pvalue_filter, interaction_filter=interaction_filter
            )
        }
        metadata = self.metadata
        network = {**metadata, **nodes, **links}
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
    def load_json(
        cls, fpath: Optional[str] = None, raw_data: Optional[dict] = None
    ) -> "Network":
        """
        Create a `Network` object from a network `JSON` file
        Either fpath or raw_data must be specified

        Parameters
        ----------
        fpath : str, optional
            The path to the network `JSON` file
        raw_data : dict, optional
            The raw data stored in the network `JSON` file

        Returns
        -------
        Network
            The instance of the `Network` class
        """
        if not raw_data and not fpath:
            raise ValueError("Either fpath or raw_data must be specified")
        if not raw_data and fpath:
            with open(fpath, "r") as fid:
                data = simplejson.load(fid)
        else:
            data = raw_data
        # Validation
        nodes_model = NodesModel({"nodes": data["nodes"]}, strict=False)
        nodes_model.validate()
        links_model = LinksModel({"links": data["links"]}, strict=False)
        links_model.validate()
        non_meta_keys = ["nodes", "links"]
        metadata = {k: v for k, v in data.items() if k not in non_meta_keys}
        networkmetadata_model = NetworkmetadataModel(metadata, strict=False)
        networkmetadata_model.validate()
        # Variable assignment
        cmetadata = data["computational_metadata"]
        interaction_type = data["interaction_type"]
        interaction_threshold = cmetadata["interaction_threshold"]
        pvalue_threshold = cmetadata["pvalue_threshold"]
        pvalue_correction = None
        directed = data["directionality"] == "directed"
        nodes: List[str] = []
        links: List[LinkDType] = []
        lineages: List[dict] = []
        children_map: Dict[str, List[str]] = {}
        for node in data["nodes"]:
            nodes.append(node["id"])
            lineage = Lineage.from_str(node["lineage"]).to_dict("Species")
            children_map[node["id"]] = node["children"]
            abundance = node.get("abundance", np.nan)
            if abundance is not None:
                lineages.append({**lineage, **dict(Abundance=abundance)})
            else:
                lineages.append(lineage)
        obs_metadata = pd.DataFrame(lineages, index=nodes)
        for link in data["links"]:
            source, target = link["source"], link["target"]
            if link["weight"] is None:
                weight = np.nan
            else:
                weight = link["weight"]
            if link["pvalue"] is None:
                pvalue = np.nan
            else:
                pvalue = link["pvalue"]
            links.append((source, target, {"weight": weight, "pvalue": pvalue}))
        network = cls(
            nodes,
            links,
            metadata,
            cmetadata,
            obs_metadata,
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
        elist: pd.DataFrame = pd.read_csv(elist_file, na_filter=False)
        elist_type = ElistType()
        elist_type.validate(elist)
        nodes = list(set([*elist["source"], *elist["target"]]))
        links: List[LinkDType] = []
        pvalue_flag = "pvalue" in elist.columns
        for entry in elist.to_dict("records"):
            source, target, weight = entry["source"], entry["target"], entry["weight"]
            links.append(
                (
                    source,
                    target,
                    {
                        "weight": weight,
                        "pvalue": entry["pvalue"] if pvalue_flag else np.nan,
                    },
                )
            )
        with open(meta_file, "r") as fid:
            metadata = simplejson.load(fid)
        with open(cmeta_file, "r") as fid:
            cmetadata = simplejson.load(fid)
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
                children_map = simplejson.load(fid)
        else:
            children_map = None
        network = cls(
            nodes,
            links,
            metadata,
            cmetadata,
            obs_metadata,
            children_map,
            interaction_type,
            interaction_threshold,
            pvalue_threshold,
            pvalue_correction,
            directed,
        )
        return network

    @classmethod
    def load_graph(cls, graph: Union[nx.Graph, nx.DiGraph]) -> "Network":
        """
        Load `Network` object from a `networkx` graph

        Parameters
        ----------
        graph : Union[nx.Graph, nx.DiGraph]
            The networkx graph of the network

        Returns
        -------
        Network
            The instance of the `Network` class
        """
        graph_md = graph.graph
        directed: bool = True if graph_md["directionality"] == "directed" else False
        interaction_type = graph_md["interaction_type"]
        cmetadata = graph_md["computational_metadata"]
        interaction_threshold = cmetadata["interaction_threshold"]
        pvalue_threshold = cmetadata["pvalue_threshold"]
        pvalue_correction = None

        metadata = graph_md
        networkmetadata_model = NetworkmetadataModel(metadata, strict=False)
        networkmetadata_model.validate()

        nodes: List[str] = []
        links: List[LinkDType] = list(graph.edges(data=True))
        lineages: List[dict] = []
        children_map: Dict[str, List[str]] = {}

        for node, ndata in graph.nodes(data=True):
            nodes.append(node)
            lineage = Lineage.from_str(ndata["lineage"]).to_dict("Species")
            children_map[node] = ndata["children"]
            abundance = ndata.get("abundance", np.nan)
            if abundance is not None:
                lineages.append({**lineage, **dict(Abundance=abundance)})
            else:
                lineages.append(lineage)
        obs_metadata = pd.DataFrame(lineages, index=nodes)

        network = cls(
            nodes,
            links,
            metadata,
            cmetadata,
            obs_metadata,
            children_map,
            interaction_type=interaction_type,
            interaction_threshold=interaction_threshold,
            pvalue_threshold=pvalue_threshold,
            pvalue_correction=pvalue_correction,
            directed=directed,
        )
        return network
