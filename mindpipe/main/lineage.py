"""
    Module that implements the `Lineage` class and  methods to work with taxonomy data
"""


from collections import namedtuple


BaseLineage = namedtuple(
    "Lineage",
    "Phylum Class Order Family Genus Species"
)


class Lineage(BaseLineage):
    """
        `NamedTuple` that stores the lineage of a taxon and methods to interact with it

        Attributes
        ----------
        Phylum: str
        Class: str
        Order: str
        Family: str
        Genus: str
        Species: str
    """
    def __new__(
            cls,
            Phylum: str = '',
            Class: str = '',
            Order: str = '',
            Family: str = '',
            Genus: str = '',
            Species: str = ''
    ) -> "Lineage":
        tax_order = [Phylum, Class, Order, Family, Genus, Species]
        empty = [i for i, tax in enumerate(tax_order) if tax == '']
        if len(tax_order) - empty[0] != len(empty):
            raise ValueError("Lower levels should not be filled if higher levels are empty")
        else:
            return super().__new__(cls, Phylum, Class, Order, Family, Genus, Species)

    def __sub__(self, other: "Lineage") -> "Lineage":
        """
            Returns the lineage that is in common between two lineages

            Parameters
            ----------
            other : "Lineage"

            Returns
            -------
            Lineage
                Common lineage
        """
        for i, (s_lin, o_lin) in enumerate(zip(self, other)):
            if s_lin != o_lin:
                return Lineage(*s_lin[:i])
        return Lineage(*self._fields)
