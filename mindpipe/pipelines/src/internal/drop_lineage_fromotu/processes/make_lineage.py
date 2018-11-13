#!/usr/bin/env python3

"""
    Script that formats the raw lineage data obtained from the OTU table into a csv file
    #OTU_ID,phylum,class,order,family,genus,species
"""

import csv
from typing import Iterable, Tuple, Dict


CLASS_ORDER = ("p", "c", "o", "f", "g", "s")
CLASSES = {
    "p": "phylum",
    "c": "class",
    "o": "order",
    "f": "family",
    "g": "genus",
    "s": "species",
}


def extract_data(fname: str) -> Iterable[Tuple[str, str]]:
    """
        Extract data from the raw lineage information

        Parameters
        ---------
        fname : str
            The absolute path to the raw lineage information

        Yields
        ------
        Tuple[str, str]
            Tuple of (OTU_ID, Consensus Lineage)
    """
    with open(fname, "r") as fid:
        next(fid)
        for line in fid:
            yield tuple(line.strip().split(" ", 1))


def parse_lineage(raw_lineage_txt: str) -> Dict[str, str]:
    """
        Parses the raw lineage and returns the dictionary of parsed lineage

        Parameters
        ---------
        raw_lineage_txt : str
            Raw lineage information

        Returns
        ------
        Dict[str, str]
            Dictionary of parsed lineage
    """
    _, *lineage_list = raw_lineage_txt.split(";")
    lineage_data: Dict[str, str] = dict(
        map(lambda x: x.strip().split("__"), lineage_list)
    )
    lineage_dict: Dict[str, str] = dict()
    for level in CLASS_ORDER:
        lineage_dict[CLASSES[level]] = lineage_data.get(level, "")
    return lineage_dict


# TODO: Make csv file


def read_data(lineage_file: str) -> Iterable[Tuple[str, Dict[str, str]]]:
    """
        Read data from the raw lineage information

        Parameters
        ---------
        fname : str
            The absolute path to the raw lineage information

        Yields
        -----
        Tuple[str, Dict[str, str]]
            Tuple of (otu_id, lineage_dict)
    """
    for otu_id, raw_lineage in extract_data(lineage_file):
        lineage_dict = parse_lineage(raw_lineage)
        yield otu_id, lineage_dict


def main(file_id: str, lineage_file: str) -> None:
    """
        Main function:
        Reads raw lineage information and writes to new csv file
    """
    fname = file_id + "_taxondata.csv"
    with open(fname, "w") as fid:
        csv_writer = csv.writer(fid, delimiter=",")
        csv_writer.writerow(
            ["#OTU_ID", "phylum", "class", "order", "family", "genus", "species"]
        )
        for otu_id, lineage_dict in read_data(lineage_file):
            csv_writer.writerow(
                [otu_id] + [lineage_dict[CLASSES[l]] for l in CLASS_ORDER]
            )
    return None


if __name__ == "__main__":
    FILE_ID = "$id"
    LINEAGE_FILE = "$lineage_file"
    main(FILE_ID, LINEAGE_FILE)
