#!/usr/bin/env python

from mindpipe import Otu


def main(biom_file, base_name):
    otu_biom = Otu.load_data(biom_file)
    otu_biom.write(base_name=base_name, file_type="tsv")


if __name__ == "__main__":
    BIOM_FILE = "$otu_file"
    BASE_NAME = "$level"
    main(BIOM_FILE, BASE_NAME)
