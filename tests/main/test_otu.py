"""
    Module containing tests for the Otu class
"""

import numpy as np
import pytest

from mindpipe.main import Otu


@pytest.mark.usefixtures("biom_data", "biom_files", "tsv_files", "stool_biom")
class TestOtu:
    """ Tests for the Otu class """

    def test_init(self, biom_data):
        for biom in biom_data:
            otu_inst = Otu(biom)
            assert (otu_inst.otu_data.to_dataframe() == biom.to_dataframe()).any().any()

    def test_load_data_biom(self, biom_files):
        for biom in biom_files["good"]:
            otu_inst = Otu.load_data(biom)
            assert hasattr(otu_inst, "otu_data")
            assert hasattr(otu_inst, "sample_metadata")
            assert hasattr(otu_inst, "obs_metadata")

    def test_load_data_tsv(self, tsv_files):
        for otu, sample, tax in tsv_files["good"]:
            otu_inst = Otu.load_data(otu, sample, tax, dtype="tsv")
            assert hasattr(otu_inst, "otu_data")
            assert hasattr(otu_inst, "sample_metadata")
            assert hasattr(otu_inst, "obs_metadata")
