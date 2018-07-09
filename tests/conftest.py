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
    biom_fol = TEST_DATADIR / "biom"
    data = {
        "good": list(biom_fol.glob("good/*.biom")),
        "bad": list(biom_fol.glob("bad/*.biom"))
    }
    return data
