"""
    Module containing tests for the Network class
"""

import json

import pytest
import pandas as pd
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

    def test_load_from_network(self, network_files):
        assert True
