"""
    Module containing tests for the taxmetdata_converter
"""

import pandas as pd
import pytest

from micone.conversion import TAX_CONVERTERS
from micone.validation.otu_schema import ObsmetaType


@pytest.mark.usefixtures("tax_conversion_data", "tmpdir")
class TestTaxmetaConverter:
    """ Tests for the taxmetdata_converter """

    def test_qiime2_to_default(self, tax_conversion_data, tmpdir):
        in_file = tax_conversion_data["qiime2"]
        out_file = tmpdir.join("default.csv")
        converter = TAX_CONVERTERS[("qiime2", "default")]
        converter(in_file, out_file)
        obsmeta_type = ObsmetaType()
        obs_metadata = pd.read_csv(out_file, index_col=0, na_filter=False)
        obsmeta_type.validate(obs_metadata)
