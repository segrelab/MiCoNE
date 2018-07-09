"""
    Module containing tests for the BiomType class
"""

from biom import load_table
import pytest
from schematics.exceptions import ValidationError

from mindpipe.validation import BiomType


@pytest.mark.usefixtures("biom_data")
class TestBiomType:
    """ Tests for the BiomType class """

    def test_init_biom_good(self, biom_data):
        biom_type = BiomType()
        for good_biom in biom_data["good"]:
            assert biom_type.validate(load_table(good_biom))

    def test_init_biom_bad(self, biom_data):
        biom_type = BiomType()
        for bad_biom in biom_data["bad"]:
            if 'empty' in str(bad_biom):
                with pytest.raises(ValueError):
                    assert biom_type.validate(load_table(bad_biom))
            if 'obs_metadata' in str(bad_biom):
                with pytest.raises(ValidationError):
                    assert biom_type.validate(load_table(bad_biom))
