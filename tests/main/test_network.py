"""
    Module containing tests for the Network class
"""

import json

import networkx as nx
import pandas as pd
import pytest

from micone.main import Network


@pytest.mark.usefixtures("raw_network_data", "correlation_files", "network_elist_files")
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
class TestNetwork:
    """ Tests for the Network class """

    def test_init(self, raw_network_data):
        for (
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
        ) in raw_network_data["good"]:
            network = Network(
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
            assert len(nodes) == len(network.nodes)
            assert len(links) == len(network.links)
            assert len(network.filter_links(True, True)) <= len(network.links)
            assert all(key in network.metadata for key in metadata)

    def test_load_data(self, correlation_files):
        for (
            corr_file,
            pval_file,
            meta_file,
            child_file,
            obsmeta_file,
            cmeta_file,
        ) in correlation_files["good"]:
            network = Network.load_data(
                corr_file, meta_file, cmeta_file, obsmeta_file, pval_file, child_file
            )
            corr_data = pd.read_table(corr_file, index_col=0)
            with open(meta_file, "r") as fid:
                meta_data = json.load(fid)
            n_nodes = corr_data.shape[0]
            assert n_nodes == len(network.nodes)
            assert (n_nodes ** 2 - n_nodes) // 2 == len(network.links)
            assert len(network.filter_links(True, True)) <= len(network.links)
            assert all(key in network.metadata for key in meta_data)

    def test_graph(self, correlation_files):
        for (
            corr_file,
            pval_file,
            meta_file,
            child_file,
            obsmeta_file,
            cmeta_file,
        ) in correlation_files["good"]:
            network = Network.load_data(
                corr_file, meta_file, cmeta_file, obsmeta_file, pval_file, child_file
            )
            graph = network.graph
            assert isinstance(graph, nx.Graph)
            if network.metadata["directionality"] == "directed":
                assert isinstance(graph, nx.DiGraph)
            assert len(network.nodes) == graph.number_of_nodes()
            assert len(network.links) == graph.number_of_edges()
            with open(meta_file) as fid:
                meta_data = json.load(fid)
            assert all(key in graph.graph for key in meta_data)

    def test_json(self, correlation_files):
        for (
            corr_file,
            pval_file,
            meta_file,
            child_file,
            obsmeta_file,
            cmeta_file,
        ) in correlation_files["good"]:
            network = Network.load_data(
                corr_file, meta_file, cmeta_file, obsmeta_file, pval_file, child_file
            )
            net_loaded = json.loads(network.json())
            assert net_loaded["nodes"] == network.nodes
            assert net_loaded["links"] == network.links
            net_loaded_thres = json.loads(network.json(True, True))
            assert net_loaded_thres["nodes"] == network.nodes
            assert net_loaded_thres["links"] == network.filter_links(True, True)

    def test_write_load_network(self, correlation_files, tmpdir):
        for (
            corr_file,
            pval_file,
            meta_file,
            child_file,
            obsmeta_file,
            cmeta_file,
        ) in correlation_files["good"]:
            network = Network.load_data(
                corr_file, meta_file, cmeta_file, obsmeta_file, pval_file, child_file
            )
            network_file = tmpdir.mkdir("test_write_load_network").join("network.json")
            network.write(network_file, pvalue_filter=True, interaction_filter=True)
            network_loaded = Network.load_json(network_file)
            assert network.metadata == network_loaded.metadata
            assert network.nodes == network_loaded.nodes
            assert network.filter_links(True, True) == network_loaded.filter_links(
                True, True
            )

    def test_load_elist(self, network_elist_files):
        for (
            network_file,
            elist_file,
            meta_file,
            cmeta_file,
            obsmeta_file,
            children_file,
        ) in network_elist_files["good"]:
            network_elist = Network.load_elist(
                elist_file, meta_file, cmeta_file, obsmeta_file, children_file
            )
            network_json = Network.load_json(network_file)
            assert network_elist.metadata == network_json.metadata
            nodes1 = sorted(network_elist.nodes, key=lambda x: x["id"])
            nodes2 = sorted(network_json.nodes, key=lambda x: x["id"])
            assert nodes1 == nodes2
            directionality = network_json.metadata["directionality"]
            if directionality == "directed":

                def fun(x: dict):
                    return x["source"], x["target"]

            else:

                def fun(x: dict):
                    return frozenset([x["source"], x["target"]])

            links1 = {
                fun(x): (f"{x['pvalue']:.5f}", f"{x['weight']:.5f}")
                for x in network_elist.filter_links(True, True)
            }
            links2 = {
                fun(x): (f"{x['pvalue']:.5f}", f"{x['weight']:.5f}")
                for x in network_json.filter_links(True, True)
            }
            assert links1 == links2
