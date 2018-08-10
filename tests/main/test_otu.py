"""
    Module containing tests for the Otu class
"""

import pytest

from mindpipe.main import Otu


@pytest.mark.usefixtures("biom_data", "biom_files", "tsv_files")
class TestOtu:
    """ Tests for the Otu class """

    def test_init(self, biom_data):
        for biom in biom_data:
            otu = Otu(biom)
            assert (otu.otu_data.to_dataframe() == biom.to_dataframe()).any().any()
