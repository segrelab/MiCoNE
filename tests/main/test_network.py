"""
    Module containing tests for the Network class
"""

import json

import networkx as nx
import pandas as pd
import pytest

from mindpipe.main import Network


@pytest.mark.usefixtures("correlation_data", "correlation_files", "network_files")
class TestNetwork:
    """ Tests for the Network class """

    def test_init(self, correlation_data):
        for corr_data, pval_data, meta_data, child_data, obsmeta_data, cmeta_data in correlation_data["good"]:
            network = Network(
                corr_data,
                meta_data,
                cmeta_data,
                obsmeta_data,
                pval_data,
                child_data,
            )
            n_nodes = corr_data.shape[0]
            assert n_nodes == len(network.nodes)
            assert (n_nodes ** 2 - n_nodes) // 2 == len(network.links)
            assert len(network.links_thres) <= len(network.links)
            assert all(key in network.metadata for key in meta_data)

    def test_load_data(self, correlation_files):
        for corr_file, pval_file, meta_file, child_file, obsmeta_file, cmeta_file in correlation_files["good"]:
            network = Network.load_data(
                corr_file,
                meta_file,
                cmeta_file,
                obsmeta_file,
                pval_file,
                child_file,
            )
            corr_data = pd.read_table(corr_file, index_col=0)
            with open(meta_file, 'r') as fid:
                meta_data = json.load(fid)
            n_nodes = corr_data.shape[0]
            assert n_nodes == len(network.nodes)
            assert (n_nodes ** 2 - n_nodes) // 2 == len(network.links)
            assert len(network.links_thres) <= len(network.links)
            assert all(key in network.metadata for key in meta_data)

    def test_graph(self, correlation_data):
        for corr_data, pval_data, meta_data, child_data, obsmeta_data, cmeta_data in correlation_data["good"]:
            network = Network(
                corr_data,
                meta_data,
                cmeta_data,
                obsmeta_data,
                pval_data,
                child_data,
            )
            graph = network.graph
            assert isinstance(graph, nx.Graph)
            if network.metadata["directionality"] == "directed":
                assert isinstance(graph, nx.DiGraph)
            assert len(network.nodes) == graph.number_of_nodes()
            assert len(network.links) == graph.number_of_edges()
            assert all(key in graph.graph for key in meta_data)

    def test_json(self, correlation_data):
        for corr_data, pval_data, meta_data, child_data, obsmeta_data, cmeta_data in correlation_data["good"]:
            network = Network(
                corr_data,
                meta_data,
                cmeta_data,
                obsmeta_data,
                pval_data,
                child_data,
            )
            net_loaded = json.loads(network.json(threshold=False))
            net_loaded["nodes"] == network.nodes
            net_loaded["links"] == network.links
            net_loaded_thres = json.loads(network.json(threshold=True))
            net_loaded_thres["nodes"] == network.nodes
            net_loaded_thres["links"] == network.links_thres
    def test_load_from_network(self, network_files):
        assert True
