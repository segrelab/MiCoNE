#!/usr/bin/env python3

# Script that groups OTU data on different taxa levels

import json
from typing import Tuple

from micone import Otu


# Group the otu_data on all the tax_levels
def grp_otu_data(otu_data: Otu, tax_level: str) -> Tuple[Otu, dict]:
    child_otu, child_groups = otu_data.collapse_taxa(tax_level)
    return child_otu, child_groups


if __name__ == "__main__":
    TAX_LEVEL: str = "${tax_level}"  # ['Family', 'Genus', 'Species']
    OTU_FILE = "${otu_file}"  # "otu.biom"
    OTU_DATA = Otu.load_data(OTU_FILE)
    child_otu, child_groups = grp_otu_data(OTU_DATA, TAX_LEVEL)
    fname = "${new_meta.id}"
    child_otu.write(fname, file_type="biom")
    with open(fname + "_children.json", "w") as fid:
        json.dump(child_groups, fid, indent=2, sort_keys=True)
