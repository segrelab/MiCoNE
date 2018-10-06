"""
    Module that implements the `Lineage` class and  methods to work with taxonomy data
"""


from collections import namedtuple
from typing import Dict, Tuple
from warnings import warn

from ete3 import NCBITaxa


BaseLineage = namedtuple(
    "Lineage",
    "Kingdom Phylum Class Order Family Genus Species"
)

NCBI = NCBITaxa()


class Lineage(BaseLineage):
    """
        `NamedTuple` that stores the lineage of a taxon and methods to interact with it

        Attributes
        ----------
        Kingdom: str
        Phylum: str
        Class: str
        Order: str
        Family: str
        Genus: str
        Species: str
    """
    def __new__(
            cls,
            Kingdom: str = '',
            Phylum: str = '',
            Class: str = '',
            Order: str = '',
            Family: str = '',
            Genus: str = '',
            Species: str = ''
    ) -> "Lineage":
        tax_order = [Kingdom, Phylum, Class, Order, Family, Genus, Species]
        empty = [i for i, tax in enumerate(tax_order) if tax == '']
        if empty and (len(tax_order) - empty[0] != len(empty)):
            raise ValueError("Lower levels should not be filled if higher levels are empty")
        else:
            norm_taxa = [cls._normalize_tax(i) for i in tax_order]
            return super().__new__(cls, *norm_taxa)

    @staticmethod
    def _normalize_tax(tax: str) -> str:
        """
            Normalize taxonomy name by removing unwanted characters

            Parameters
            ----------
            tax : str

            Returns
            -------
            str
                Normalized taxonomy name
        """
        return tax.strip().strip('[]')

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
                return Lineage(*self[:i])
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
        return 'Kingdom', ''

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
                tax_list = lineage_str.split(';')
            elif lineage_str.startswith('p'):
                tax_list = ['Bacteria'] + lineage_str.split(';')
            else:
                raise ValueError("Incompatible lineage string")
        elif style == "silva":
            if lineage_str.startswith('D_0'):
                tax_list = lineage_str.split(';D_7')[0].split(';')
            elif lineage_str.startswith('D_1'):
                tax_list = ['Bacteria'] + lineage_str.split(';D_7')[0].split(';')
            else:
                raise ValueError("Incompatible lineage string")
        else:
            raise ValueError("Style has to be either 'gg' or 'silva'")
        taxa = [l.strip().rsplit('__', 1)[-1] for l in tax_list]
        return cls(*taxa)

    def to_str(self, style: str, level: str) -> str:
        """
            Return the string Lineage of the instance in requested 'style'

            Parameters
            ----------
            style : {'gg', 'silva'}
                The style of the lineage string
            level : str
                The lowest Lineage field that is to be populated

            Returns
            -------
            str
        """
        if level not in self._fields:
            raise ValueError(f"{level} not a valid field for Lineage")
        else:
            ind = self._fields.index(level)
            fields = self._fields[:ind + 1]
            data = self[:ind + 1]
        if style == "gg":
            prefix = [f.lower()[0] for f in fields]
        elif style == "silva":
            prefix = [f"D_{i}" for i in range(len(fields))]
        else:
            raise ValueError("Style needs to be either 'gg' or 'silva'")
        return ';'.join(f"{p}__{v}" for p, v in zip(prefix, data))

    def __str__(self) -> str:
        """
            Get the lineage in the form of a string

            Returns
            -------
            str
                The lineage string in 'gg' format
        """
        return self.to_str(style="gg", level="Species")

    def to_dict(self, level: str) -> Dict[str, str]:
        """
            Get the lineage in the form of a dictionary

            Parameters
            ----------
            level : str
                The lowest Lineage field to be used to populate the dictionary
        """
        if level not in self._fields:
            raise ValueError(f"{level} not a valid field for Lineage")
        ind = self._fields.index(level)
        fields = self._fields[:ind + 1]
        return {field: tax for field, tax in zip(fields, self)}

    def get_superset(self, level: str) -> "Lineage":
        """
            Return a superset of the current lineage for the requested level

            Parameters
            ----------
            level : str
                The lowest Lineage field to be used to calculate the superset

            Returns
            -------
            Lineage
                Lineage instance that is a superset of current instance
        """
        if level not in self._fields:
            raise ValueError(f"{level} not a valid field for Lineage")
        ind = self._fields.index(level)
        tax = self[:ind + 1]
        return Lineage(*tax)

    @property
    def taxid(self) -> int:
        """
            Get the NCBI taxonomy id of the Lineage

            Returns
            -------
            int
                The NCBI taxonomy id
        """
        # FIXME: I think get name translator expects a string like "Escherichia coli" not separated
        taxid_dict = NCBI.get_name_translator(self)
        try:
            taxid_list = taxid_dict[self.name[1]]
        except KeyError:
            warn(f"Lowest level in {self} could not be queried. Using higher level")
            low_ind = self.index(self.name[1])
            # NOTE: If this fails again the program will crash
            taxid_list = taxid_dict[self[low_ind - 1]]
        if len(taxid_list) > 1:
            warn(f"{self.name} has multiple taxids. Picking the first one")
        taxid = taxid_list[0]
        return taxid
