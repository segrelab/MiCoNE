"""
    Module containing tests for the Network class
"""

import pytest

from mindpipe.main import Network


@pytest.mark.usefixtures("correlation_data", "correlation_files", "network_files")
class TestNetwork:
    """ Tests for the Network class """

    def test_init(self, correlation_data):
        cmetadata = {}
        for corr_data, pval_data, meta_data, child_data, obsmeta_data in correlation_data["good"]:
            assert Network(
                corr_data,
                meta_data,
                cmetadata,
                obsmeta_data,
                pval_data,
                child_data,
            )

    def test_load_data(self, correlation_files):
        assert True

    def test_load_from_network(self, network_files):
        assert True
