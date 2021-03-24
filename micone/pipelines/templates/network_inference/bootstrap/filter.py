#!/usr/bin/env python

import glob
import os
import shutil

import pandas as pd


def main(file_glob, filter_flag):
    files = glob.glob(file_glob)
    filtered_dir = "filtered"
    os.mkdir(filtered_dir)
    for file in files:
        df = pd.read_table(file, index_col=0)
        obs_reject_flag = (df.sum(axis=1) == 0).any()
        sample_reject_flag = (df.sum(axis=0) == 0).any()
        if not filter_flag:
            obs_reject_flag = False
            sample_reject_flag = False
        if obs_reject_flag or sample_reject_flag:
            print("Rejected ", file)
        else:
            new_file = filtered_dir + "/" + os.path.basename(file).split(".temp")[0]
            shutil.copy(file, new_file)


if __name__ == "__main__":
    FILE_GLOB = "*.boot.temp"
    FILTER_FLAG = True if "${filter_flag}" == "True" else False
    main(FILE_GLOB, FILTER_FLAG)
