#!/usr/bin/env python3

import csv
from typing import Iterable


def read_data(observation_file: str) -> Iterable[str]:
    """
        Read data from raw observation file

        Parameters
        ---------
        observation_file : str
            The absolute path to the raw observation file

        Yields
        -----
        str
            Observation id
    """
    with open(observation_file, "r") as fid:
        observations = fid.readline().strip().split(" ")
    yield from observations


def main(file_id: str, obs_file: str) -> None:
    """
        Main function:

    """
    file_name = file_id + "_sample_metadata.csv"
    with open(file_name, "w") as fid:
        csv_writer = csv.writer(fid, delimiter=",")
        csv_writer.writerow(["#Sample_ID", "metadata"])
        for observation_id in read_data(obs_file):
            csv_writer.writerow([observation_id, file_id])


if __name__ == "__main__":
    FILE_ID = "$id"
    OBS_FILE = "$obs_file"
    main(FILE_ID, OBS_FILE)
