#!/usr/bin/env python

from mindpipe import Otu


def main(biom_file, id_):
    otu_biom = Otu.load_data(biom_file)
    otu_biom.write(base_name=id_, file_type="tsv")


if __name__ == "__main__":
    BIOM_FILE = "$otu_file"
    ID = "$id"
    main(BIOM_FILE, ID)
