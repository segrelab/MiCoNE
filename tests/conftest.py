"""
    Common configuration for all the tests
"""

import pathlib

import pytest


BASEDIR = pathlib.Path.cwd()
TEST_DATADIR = BASEDIR / "tests/data"


@pytest.fixture(scope="module")
def biom_data():
    """ Fixture that loads biom data """
    biom_fol = TEST_DATADIR / "otus/biom"
    data = {
        "good": list(biom_fol.glob("good/*.biom")),
        "bad": list(biom_fol.glob("bad/*.biom"))
    }
    return data

@pytest.fixture(scope="module")
def tsv_data():
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
