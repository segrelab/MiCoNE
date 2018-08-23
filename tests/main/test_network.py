"""
    Module containing tests for the Network class
"""

import pytest

from mindpipe.main import Network


@pytest.mark.usefixtures("correlation_data", "correlation_files", "network_files")
class TestNetwork:
    """ Tests for the Network class """

    def test_init(self, correlation_data):
        for corr_data, pval_data, meta_data, child_data, obsmeta_data, cmeta_data in correlation_data["good"]:
            assert Network(
                corr_data,
                meta_data,
                cmeta_data,
                obsmeta_data,
                pval_data,
                child_data,
            )

    def test_load_data(self, correlation_files):
        for corr_file, pval_file, meta_file, child_file, obsmeta_file, cmeta_file in correlation_files["good"]:
            assert Network.load_data(
                corr_file,
                meta_file,
                cmeta_file,
                obsmeta_file,
                pval_file,
                child_file,
            )

    def test_load_from_network(self, network_files):
        assert True
