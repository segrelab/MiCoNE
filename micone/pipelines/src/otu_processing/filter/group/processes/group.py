#!/usr/bin/env python3

# Script that groups OTU data on different taxa levels

import json
from typing import List, Iterable, Tuple

from micone import Otu, Lineage


# Group the otu_data on all the tax_levels
def grp_otu_data(otu_data: Otu, tax_levels: List[str]) -> Iterable[Tuple[Otu, dict]]:
    sorted_tax_levels = list(reversed(tax_levels))
    child_otu = otu_data
    for tax_level in sorted_tax_levels:
        child_otu, child_groups = child_otu.collapse_taxa(tax_level)
        yield child_otu, child_groups


if __name__ == "__main__":
    TAX_LEVELS: List[str] = $tax_levels  # ['Family', 'Genus', 'Species']
    OTU_FILE = "$otu_file"  # "otu.biom"
    otu_data = Otu.load_data(OTU_FILE)
    for child_otu, child_groups in grp_otu_data(otu_data, TAX_LEVELS):
        fname = child_otu.tax_level + "_level"
        child_otu.write(fname, file_type="biom")
        with open(fname + "_children.json", "w") as fid:
            json.dump(child_groups, fid, indent=2, sort_keys=True)
