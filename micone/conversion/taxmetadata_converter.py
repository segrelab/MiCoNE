"""
    Module containing methods that convert taxonomy metadata into various formats
"""

import csv
import pathlib
from typing import Dict, List

import pandas as pd

from ..validation.otu_schema import ObsmetaType
from ..main import Lineage


def qiime2_to_default(in_file: pathlib.Path, out_file: pathlib.Path) -> None:
    """
    Convert Taxonomy metadata file from qiime2 to default format

    Parameters
    ----------
    in_file : pathlib.Path
        The path to the qiime2 formatted input file
    out_file : pathlib.Path
        The path to the default format output file
    """
    with open(in_file, "r") as fid:
        csv_reader = csv.reader(fid, delimiter="\t")
        data_dict: Dict[str, List[str]] = {key: [] for key in ObsmetaType._req_keys}
        data_dict["ID"] = []
        header, *rest = csv_reader
        ekey = ObsmetaType._extra_keys[0]  # the Confidence value
        if ekey in header:
            data_dict[ekey] = []
        for line in rest:
            if line[0].startswith("#q2:types"):
                continue
            lineage = Lineage.from_str(line[header.index("Taxon")])
            data_dict["ID"].append(line[0])
            for rkey in ObsmetaType._req_keys:
                data_dict[rkey].append(getattr(lineage, rkey))
            if ekey in data_dict:
                data_dict[ekey].append(line[header.index(ekey)])
    df = pd.DataFrame.from_dict(data_dict)
    df.set_index("ID", inplace=True, verify_integrity=True)
    df.to_csv(out_file, index=True)


def qiime1_to_default(in_file: pathlib.Path, out_file: pathlib.Path) -> None:
    """
    Convert Taxonomy metadata file from qiime1 to default format

    Parameters
    ----------
    in_file : pathlib.Path
        The path to the qiime1 formatted input file
    out_file : pathlib.Path
        The path to the default format output file
    """
    pass


def default_to_qiime2(in_file: pathlib.Path, out_file: pathlib.Path) -> None:
    """
    Convert Taxonomy metadata file from default format to qiime2

    Parameters
    ----------
    in_file : pathlib.Path
        The path to the default format input file
    out_file : pathlib.Path
        The path to the qiime2 formatted output file
    """
    pass


CONVERTERS = {
    ("qiime2", "default"): qiime2_to_default,
    ("qiime1", "default"): qiime1_to_default,
    ("default", "qiime2"): default_to_qiime2,
}
