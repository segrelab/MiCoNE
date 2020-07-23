"""
    Module containing methods that convert networks into various formats
"""

import pathlib

import pandas as pd

from ..main import Network


def json_to_elist(in_file: pathlib.Path, out_file: pathlib.Path) -> None:
    """
        Convert Network file from json to elist format
        Note that only the edge attributes can be converted

        Parameters
        ----------
        in_file : pathlib.Path
            The path to the json formatted network file
        out_file : pathlib.Path
            The path to the elist formatted network file
    """
    network = Network.load_json(in_file)
    df = pd.DataFrame.from_dict(network.links)
    cols = list(df.columns)
    cols.remove("source")
    cols.remove("target")
    df = df[["source", "target"] + cols]
    df.to_csv(out_file, index=False)


CONVERTERS = {("json", "elist"): json_to_elist}
