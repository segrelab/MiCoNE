"""
    Module that implements the `Lineage` class and  methods to work with taxonomy data
"""


from collections import namedtuple
from typing import Tuple


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

    @property
    def name(self) -> Tuple[str, str]:
        """
            Get the lowest populated level and name of the taxon

            Returns
            -------
            Tuple[str, str]
                Tuple containing (level, name)
        """
        fields = self._fields
        for field in reversed(fields):
            ind = fields.index(field)
            name = self[ind]
            if name != '':
                return field, name
        return 'Phylum', ''

    @classmethod
    def from_str(cls, lineage_str: str, style: str = "gg") -> "Lineage":
        """
            Create `Lineage` instance from a lineage string

            Parameters
            ----------
            lineage_str : str
                Lineage in the form of a string
            style : {'gg', 'silva'}, optional
                The style of the lineage string
                Default is 'gg'

            Returns
            -------
            Lineage
                Instance of the `Lineage` class
        """
        if style == "gg":
            if lineage_str.startswith('k'):
                tax_list = lineage_str.split(';', 1)[-1].split(';')
            elif lineage_str.startswith('p'):
                tax_list = lineage_str.split(';')
            else:
                raise ValueError("Incompatible lineage string")
        elif style == "silva":
            if lineage_str.startswith('D_0'):
                tax_list = lineage_str.split(';', 1)[-1].split(';D_7')[0].split(';')
            elif lineage_str.startswith('D_1'):
                tax_list = lineage_str.split(';D_7')[0].split(';')
            else:
                raise ValueError("Incompatible lineage string")
        else:
            raise ValueError("Style has to be either 'gg' or 'silva'")
        taxa = [l.strip().rsplit('__', 1)[-1] for l in tax_list]
        return cls(*taxa)
