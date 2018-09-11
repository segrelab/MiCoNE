"""
    Common configuration for all the tests
"""

import json
import pathlib

from biom import load_table
import pandas as pd
import pytest


BASEDIR = pathlib.Path.cwd()
TEST_DATADIR = BASEDIR / "tests/data"
PIPELINE_DIR = BASEDIR / "mindpipe/pipelines/src"


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
            obsmeta = data_fol / "obs_metadata.csv"
            cmeta = data_fol / "cmetadata.json"
            data[kind].append((corr, pval, meta, child, obsmeta, cmeta))
    return data


@pytest.fixture(scope="module")
def correlation_data(correlation_files):
    """ Fixture that creates the inputs for the network class """
    data = {"good": [], "bad": []}
    for kind in ("good", "bad"):
        for corr, pval, meta, child, obsmeta, cmeta in correlation_files[kind]:
            corr_data = pd.read_table(corr, index_col=0)
            pval_data = pd.read_table(pval, index_col=0)
            obsmeta_data = pd.read_csv(obsmeta, index_col=0, na_filter=False)
            with open(meta, 'r') as fid:
                meta_data = json.load(fid)
            with open(child, 'r') as fid:
                child_data = json.load(fid)
            with open(cmeta, 'r') as fid:
                cmeta_data = json.load(fid)
            data[kind].append((corr_data, pval_data, meta_data, child_data, obsmeta_data, cmeta_data))
    return data


@pytest.fixture(scope="module")
def network_json_files():
    """ Fixture that loads the network files """
    net_fol = TEST_DATADIR / "networks"
    data = {
        "good": net_fol.glob("good/*.json"),
        "bad": net_fol.glob("bad/*json")
    }
    return data


@pytest.fixture(scope="module")
def raw_network_data(network_json_files):
    """ Fixture that loads the network file directly as json """
    data = {"good": [], "bad": []}
    for kind in {"good", "bad"}:
        for file in network_json_files[kind]:
            with open(file, 'r') as fid:
                data[kind].append(json.load(fid))
    return data


@pytest.fixture(scope="module")
def network_elist_files():
    """ Fixture that loads the network elist files """
    net_fol = TEST_DATADIR / "networks"
    data = {"good": [], "bad": []}
    for kind in ("good", "bad"):
        network = net_fol / kind / "network.json"
        elist_fol = net_fol / kind / "elist"
        elist = elist_fol / "elist.csv"
        meta = elist_fol / "metadata.json"
        cmeta = elist_fol / "cmetadata.json"
        obsmeta = elist_fol / "obs_metadata.csv"
        children = elist_fol / "children_map.json"
        data[kind].append((network, elist, meta, cmeta, obsmeta, children))
    return data


@pytest.fixture(scope="module")
def config_template_files():
    """ Fixture for the config template files """
    template_file = {
        "input": TEST_DATADIR / "templates/config/sparcc.j2",
        "output": TEST_DATADIR / "templates/config/sparcc.config"
    }
    data = {
        "compute_correlations": {
            "niters": 10,
        },
        "resampling": {
            "nboots": 100,
        },
        "output_dir": "results",
        "input": {
            "otu_table": "/testing/data/otudata.tsv",
            "lineage_table": "/testing/data/lineagedata.csv",
            "sample_metadata": "/testing/data/sample_metadata.csv",
            "children_object": "/testing/data/children.json",
        }
    }
    return template_file, data


@pytest.fixture(scope="module")
def script_template_files():
    """ Fixture for the script template files """
    template_file = {
        "input": TEST_DATADIR / "templates/script/sparcc.j2",
        "output": TEST_DATADIR / "templates/script/sparcc.nf"
    }
    process_folder = TEST_DATADIR / "templates/script/templates"
    return template_file, process_folder
