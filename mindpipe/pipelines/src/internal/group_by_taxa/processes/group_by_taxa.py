#!/usr/bin/env python3

'''
    Script that
    1. Removes sparse OTUs and samples based on flag
    2. Group OTU data on different taxa levels
    3. Connect the various groups to each other using the `map_children` method
'''

from mind.main.otu import OtuClass, CollapsedOtuClass
from toolz import sliding_window
from typing import List, Iterable, Dict


def rm_sparse_data(otu_data: OtuClass, sparse_otus: bool, sparse_samples: bool) -> OtuClass:
    '''
        Remove sparse OTUs and/or samples from the OTU file

        Parameters
        ---------
        otu_file : OtuClass
            Raw OtuClass instance
        sparse_otus : bool
            Flag that determines whether or not to remove sparse otus
        sparse_samples : bool
            Flag that determines whether or not to remove sparse samples

        Returns
        ------
        OtuClass
            OtuClass instance with sparse data removed
    '''
    # first remove sparse otus
    if sparse_otus:
        otu_data = otu_data.rm_sprse_otus()  # NOTE: We can pass these parameters in as well
    # second remove sparse samples
    if sparse_samples:
        otu_data = otu_data.rm_sprse_samples()
    return otu_data


def grp_otu_data(otu_data: OtuClass, tax_levels: List[str]) -> Iterable[Dict[str, CollapsedOtuClass]]:
    '''
        Group the otu_data on all the taxa levels in tax_levels

        Parameters
        ---------
        otu_data : OtuClass
            The OtuClass instance that is to be grouped

        Yields
        ------
        Dict[str, CollpasedOtuClass]
            Dictionary of child and parent otu instances
    '''
    sorted_tax = list(reversed(tax_levels))
    child_otu = CollapsedOtuClass(**otu_data.group_on_taxondata(sorted_tax[0]))
    child_otu.write_file(child_otu.level + "_level", file_type="tsv")
    for parent_tax in sorted_tax[1:]:
        parent_otu = CollapsedOtuClass(**otu_data.group_on_taxondata(parent_tax))
        yield {
            'child': child_otu,
            'parent': parent_otu
        }
        child_otu = parent_otu


def mapper(parent_child_dict: Dict[str, CollapsedOtuClass]) -> CollapsedOtuClass:
    '''
        Maps the parent to the child OTU labels

        Parameters
        ---------
        parent_child_dict : Dict[str, CollapsedOtuClass]
            Dictionary containing the parent and child OTU class instances

        Returns
        ------
        CollapsedOtuClass
            Parent OTU class that has its OTU labels mapped to it's child
    '''
    parent_otu = parent_child_dict['parent']
    child_otu = parent_child_dict['child']
    return parent_otu.map_children(child_otu)


if __name__ == '__main__':
    RM_SPARSE_OTUS: bool = $rm_sparse_otu  # True
    RM_SPARSE_SAMPLES: bool = $rm_sparse_samples  # True
    TAX_LEVELS: List[str] = $tax_levels  # ['family', 'genus', 'species']
    OTU_FILE = "$otu_file"  # "OTU_level_otudata.tsv"
    SAMPLE_META_FILE = "$sample_meta_file"  # "OTU_level_metadata.csv"
    LINEAGE_FILE = "$lineage_file"  # "OTU_level_taxondata.csv"
    sparse_otu = rm_sparse_data(
        OtuClass.load_data(OTU_FILE, SAMPLE_META_FILE, LINEAGE_FILE),
        RM_SPARSE_OTUS,
        RM_SPARSE_SAMPLES
    )
    sparse_otu.write_file("OTU_level", file_type="tsv")
    for pc_dict in grp_otu_data(sparse_otu, TAX_LEVELS):
        mapped_otu = mapper(pc_dict)
        mapped_otu.write_file(mapped_otu.level + "_level", file_type="tsv")
