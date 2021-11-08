#!/usr/bin/env python3

import pathlib
from micone import Otu
from warnings import warn


def main(otu_file: str, axis: str, column: str):
    otu = Otu.load_data(otu_file)
    if axis != "sample":
        raise NotImplementedError("Axis other than sample are not currently supported")
    if not column:
        warn("No column supplied for splitting")
        split_results = [("", otu)]
    else:
        func = lambda id_, md: md[column]
        split_results = otu.partition(axis, func)
    return split_results


if __name__ == "__main__":
    OTU_FILE = "${otu_file}"
    AXIS = "${axis}"
    COLUMN = "${column}"
    ID_ = "${meta.id}"
    split_results = main(OTU_FILE, AXIS, COLUMN)
    folder = pathlib.Path("split")
    folder.mkdir(exist_ok=True)
    filter_fun = lambda values, id_, md: True if any(values > 0.0) else False
    for label, split_otu in split_results:
        split_otu.otu_data.del_metadata(keys=[COLUMN], axis=AXIS)
        split_otu.filter(func=filter_fun, axis="observation")
        if label == "":
            split_otu.write(ID_, fol_path=str(folder))
        elif label is None:
            raise ValueError(f"Unable to split on column {COLUMN}")
        else:
            split_otu.write(ID_ + f"-{label}", fol_path=str(folder))
