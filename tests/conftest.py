"""
    Common configuration for all the tests
"""

import pathlib

import pytest
from biom import load_table


BASEDIR = pathlib.Path.cwd()
TEST_DATADIR = BASEDIR / "tests/data"


@pytest.fixture(scope="module")
def biom_files():
    """ Fixture that loads biom data """
    biom_fol = TEST_DATADIR / "otus/biom"
    data = {
        "good": list(biom_fol.glob("good/*.biom")),
        "bad": list(biom_fol.glob("bad/*.biom"))
    }
    return data


@pytest.fixture(scope="module")
def tsv_files():
    """ Fixture that loads the tsv data """
    tsv_fol = TEST_DATADIR / "otus/tsv"
    data = {"good": [], "bad": []}
    for kind in ("good", "bad"):
        for data_fol in (tsv_fol / kind).iterdir():
            otu = data_fol / "otu.tsv"
            sample = data_fol / "sample_metadata.tsv"
            tax = data_fol / "tax_metadata.tsv"
            data[kind].append((otu, sample, tax))
    return data


@pytest.fixture(scope="module")
def lineage_data():
    """ Fixture that creates example data for lineage class """
    base = {
        "Kingdom": "Bacteria",
        "Phylum": "P1",
        "Class": "C1",
        "Order": "O1",
        "Family": "F1",
        "Genus": "G1",
        "Species": "S1",
    }
    good = {**base}
    bad = {**base}
    bad["Class"] = ""
    data = {
        "good": good,
        "bad": bad,
    }
    return data


@pytest.fixture(scope="module")
def tax_conversion_data():
    """ Fixture that loads data for testing the tax convertors """
    tsv_fol = TEST_DATADIR / "otus/tsv"
    data = {
        "qiime2": tsv_fol / "bad/bad_tax/tax_metadata.tsv",
        "qiime1": "",
        "defaul": "",
    }
    return data

@pytest.fixture(scope="module")
def biom_data(biom_files):
    """ Fixture that creates biom data """
    return [load_table(biom) for biom in biom_files["good"]]


@pytest.fixture(scope="module")
def stool_biom(biom_files):
    """ Fixture that loads the stool biom data """
    biom_file = TEST_DATADIR / "otus/biom/good/stool.biom"
    return load_table(biom_file)

@pytest.fixture(scope="module")
def correlation_files():
    """ Fixture that loads the correlation data """
    corr_fol = TEST_DATADIR / "correlations"
    data = {"good": [], "bad": []}
    for kind in ("good", "bad"):
        for data_fol in (corr_fol / kind).iterdir():
            corr = data_fol / "correlations.tsv"
            pval = data_fol / "pvalues.tsv"
            meta = data_fol / "metadata.json"
            child = data_fol / "children_map.json"
            data[kind].append((corr, pval, meta, child))
    return data
