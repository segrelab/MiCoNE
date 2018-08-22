"""
    Module containing tests for the BiomType class
"""

import json

from biom import load_table
import pandas as pd
import pytest
from schematics.exceptions import DataError, ValidationError

from mindpipe.validation import (
    BiomType,
    CorrelationmatrixType,
    PvaluematrixType,
    MetadataType,
    ChildrenmapType
)


@pytest.mark.usefixtures("biom_files")
class TestBiomType:
    """ Tests for the BiomType class """

    def test_init_biom_good(self, biom_files):
        biom_type = BiomType()
        for good_biom in biom_files["good"]:
            assert biom_type.validate(load_table(good_biom))

    def test_init_biom_bad(self, biom_files):
        biom_type = BiomType()
        for bad_biom in biom_files["bad"]:
            if 'empty' in str(bad_biom):
                with pytest.raises(ValueError):
                    assert biom_type.validate(load_table(bad_biom))
            if 'obs_metadata' in str(bad_biom):
                with pytest.raises(ValidationError):
                    assert biom_type.validate(load_table(bad_biom))

@pytest.mark.usefixtures("correlation_files")
class TestInteractionType:
    """ Tests for correlations, pvalues and their associated metadata """

    def test_correlations_good(self, correlation_files):
        corr_type = CorrelationmatrixType()
        pval_type = PvaluematrixType(symm=True)
        meta_type = MetadataType()
        children_type = ChildrenmapType()
        for corr, pval, meta, child in correlation_files["good"]:
            corr_data = pd.read_table(corr, index_col=0)
            pval_data = pd.read_table(pval, index_col=0)
            with open(meta, 'r') as fid:
                meta_data = json.load(fid)
            with open(child, 'r') as fid:
                child_data = json.load(fid)
            corr_type.validate(corr_data)
            pval_type.validate(pval_data)
            meta_type.validate(meta_data)
            children_type.validate(child_data)

    def test_correlations_bad(self, correlation_files):
        corr_type = CorrelationmatrixType()
        pval_type = PvaluematrixType(symm=True)
        children_type = ChildrenmapType()
        for corr, pval, meta, child in correlation_files["bad"]:
            corr_data = pd.read_table(corr, index_col=0)
            pval_data = pd.read_table(pval, index_col=0)
            with open(meta, 'r') as fid:
                meta_data = json.load(fid)
            with open(child, 'r') as fid:
                child_data = json.load(fid)
            with pytest.raises(ValidationError):
                corr_type.validate(corr_data)
            with pytest.raises(ValidationError):
                pval_type.validate(pval_data)
            meta_type = MetadataType(meta_data, strict=False)
            with pytest.raises(DataError):
                meta_type.validate()
            with pytest.raises(ValidationError):
                children_type.validate(child_data)
