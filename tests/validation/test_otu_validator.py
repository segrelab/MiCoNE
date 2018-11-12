"""
    Module containing tests for the OtuValidator class
"""

import pytest
from schematics.exceptions import ValidationError

from mindpipe.validation import OtuValidator


@pytest.mark.usefixtures("biom_files", "tsv_files")
class TestOtuValidator:
    """ Tests for the OtuValidator class """

    def test_init_biom_good(self, biom_files):
        biom_validator = OtuValidator(dtype="biom")
        configuration = biom_validator.configuration
        assert configuration["dtype"] == "biom"
        for good_biom in biom_files["good"]:
            assert good_biom.suffix in configuration["valid_otu_ext"]
            assert biom_validator.load_validate(good_biom)

    def test_init_biom_bad(self, biom_files):
        biom_validator = OtuValidator(dtype="biom")
        for bad_biom in biom_files["bad"]:
            if "empty" in str(bad_biom):
                with pytest.raises(ValueError):
                    biom_validator.load_validate(bad_biom)
            if "obs_metadata" in str(bad_biom):
                with pytest.raises(ValidationError):
                    biom_validator.load_validate(bad_biom)
            if "incorrect_metadata" in str(bad_biom):
                with pytest.raises(KeyError):
                    biom_validator.load_validate(bad_biom)

    def test_init_tsv_good(self, tsv_files):
        tsv_validator = OtuValidator(dtype="tsv")
        for otu, sample, tax in tsv_files["good"]:
            assert tsv_validator.load_validate(otu, sample, tax)

    def test_init_tsv_bad(self, tsv_files):
        tsv_validator = OtuValidator(dtype="tsv")
        for otu, sample, tax in tsv_files["bad"]:
            if "bad_otu" in str(otu):
                with pytest.raises(TypeError):
                    tsv_validator.load_validate(otu, sample, tax)
            if "bad_tax" in str(tax):
                with pytest.raises(ValidationError):
                    tsv_validator.load_validate(otu, sample, tax)
