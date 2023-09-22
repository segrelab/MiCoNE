#!/usr/bin/env python

import pathlib
import shutil

PROCESS = (
    "dada2-remove_bimera-naive_bayes(gg_13_8_99)-normalize_filter(on)-group(Genus)"
)
DATASET = "emp"
TO_SKIP = {"network", "mldm", "pearson", "spearman"}


def copy_raw_networkdata(data_folder: pathlib.Path, output_folder: pathlib.Path):
    for folder in data_folder.iterdir():
        method_name = folder.name
        if method_name in TO_SKIP:
            continue
        print(f"Copying folder {method_name}")
        network_folder = folder / f"{method_name}/{PROCESS}/{DATASET}"
        for file in network_folder.iterdir():
            if file.is_file():
                file_name = file.name
                output_file = output_folder / f"{method_name}/{file_name}"
                shutil.copy(file, output_file)


def copy_json_networkdata(data_folder: pathlib.Path, output_folder: pathlib.Path):
    network_folders = (
        "make_network_with_pvalue",
        "make_network_without_pvalue",
    )
    for network_folder in network_folders:
        for sub_folder in (data_folder / f"network/{network_folder}").iterdir():
            if not sub_folder.name.startswith(PROCESS):
                continue
            method_name = sub_folder.name.split("-")[-1]
            if method_name in TO_SKIP:
                continue
            print(f"Copying folder {method_name}")
            for file in (sub_folder / "emp").iterdir():
                if file.is_file():
                    file_name = file.name
                    output_file = output_folder / f"{method_name}/{file_name}"
                    shutil.copy(file, output_file)


if __name__ == "__main__":
    DATA_FOLDER = pathlib.Path("../network_inference")
    OUTPUT_FOLDER = pathlib.Path(".")
    copy_json_networkdata(DATA_FOLDER, OUTPUT_FOLDER)
