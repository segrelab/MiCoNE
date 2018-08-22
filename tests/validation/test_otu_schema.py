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
    ObsmetaType,
    CorrelationmatrixType,
    PvaluematrixType,
    MetadataModel,
    ChildrenmapType,
    NodesModel,
    LinksModel,
    NetworkmetadataModel,
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
        obsmeta_type = ObsmetaType()
        meta_type = MetadataModel()
        children_type = ChildrenmapType()
        for corr, pval, meta, child, obsmeta in correlation_files["good"]:
            corr_data = pd.read_table(corr, index_col=0)
            pval_data = pd.read_table(pval, index_col=0)
            obsmeta_data = pd.read_csv(obsmeta, index_col=0, na_filter=False)
            with open(meta, 'r') as fid:
                meta_data = json.load(fid)
            with open(child, 'r') as fid:
                child_data = json.load(fid)
            corr_type.validate(corr_data)
            pval_type.validate(pval_data)
            obsmeta_type.validate(obsmeta_data)
            meta_type.validate(meta_data)
            children_type.validate(child_data)

    def test_correlations_bad(self, correlation_files):
        corr_type = CorrelationmatrixType()
        pval_type = PvaluematrixType(symm=True)
        obsmeta_type = ObsmetaType()
        children_type = ChildrenmapType()
        for corr, pval, meta, child, obsmeta in correlation_files["bad"]:
            corr_data = pd.read_table(corr, index_col=0)
            pval_data = pd.read_table(pval, index_col=0)
            obsmeta_data = pd.read_csv(obsmeta, index_col=0, na_filter=False)
            with open(meta, 'r') as fid:
                meta_data = json.load(fid)
            with open(child, 'r') as fid:
                child_data = json.load(fid)
            with pytest.raises(ValidationError):
                corr_type.validate(corr_data)
            with pytest.raises(ValidationError):
                pval_type.validate(pval_data)
            meta_type = MetadataModel(meta_data, strict=False)
            with pytest.raises(DataError):
                meta_type.validate()
            with pytest.raises(ValidationError):
                children_type.validate(child_data)
            with pytest.raises(ValidationError):
                obsmeta_type.validate(obsmeta_data)


@pytest.mark.usefixtures("raw_network_data")
class TestNetworkType:
    """ Tests for nodes, links and network metadata models """

    def test_nodes(self, raw_network_data):
        for good_data in raw_network_data["good"]:
            good_nodes = good_data["nodes"]
            good_nodes_model = NodesModel({"nodes": good_nodes}, strict=False)
            good_nodes_model.validate()
        for bad_data in raw_network_data["bad"]:
            bad_nodes = bad_data["nodes"]
            with pytest.raises(DataError):
                bad_nodes_model = NodesModel({"nodes": bad_nodes}, strict=False)
                bad_nodes_model.validate()

    def test_links(self, raw_network_data):
        for good_data in raw_network_data["good"]:
            good_links = good_data["links"]
            good_links_model = LinksModel({"links": good_links}, strict=False)
            good_links_model.validate()
        for bad_data in raw_network_data["bad"]:
            bad_links = bad_data["links"]
            with pytest.raises(DataError):
                bad_links_model = LinksModel({"links": bad_links}, strict=False)
                bad_links_model.validate()

    def test_networkmetadata(self, raw_network_data):
        for good_data in raw_network_data["good"]:
            good_metadata = {k: v for k, v in good_data.items() if k not in {"links", "nodes"}}
            print(good_metadata)
            good_metadata_model = NetworkmetadataModel(good_metadata, strict=False)
            good_metadata_model.validate()
        for bad_data in raw_network_data["bad"]:
            bad_metadata = {k: v for k, v in bad_data.items() if k not in {"links", "nodes"}}
            with pytest.raises(DataError):
                bad_metadata_model = NetworkmetadataModel(bad_metadata, strict=False)
                bad_metadata_model.validate()
