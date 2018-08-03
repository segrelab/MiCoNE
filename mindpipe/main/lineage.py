"""
    Module that implements the `Lineage` class and  methods to work with taxonomy data
"""


from collections import namedtuple


BaseLineage = namedtuple(
    "Lineage",
    "Phylum Class Order Family Genus Species"
)

