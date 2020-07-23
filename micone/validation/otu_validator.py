"""
    Module that deals with the validation of an OTU table
"""

import pathlib
from typing import Dict, List, Optional, Union

import pandas as pd
from biom import load_table, Table

from .otu_schema import BiomType, SamplemetaType, ObsmetaType


class OtuValidator:
    """
        Validates input `OTU` table file and returns the `Otu` instance of the file

        Parameters
        ----------
        dtype : {'biom', 'tsv'}
            The type of OtuValidator instance to be created
        ext : str, optional
            The extension of the file if other than supported extensions
            Supported extensions:
            'tsv' dtype: 'tsv', 'txt', 'counts'
            'biom' dtype: 'biom', 'hdf5'

        Attributes
        ----------
        configuration : Dict[str, Any]
            Dictionary showing the current configuration of the instance
        validator : BiomType
            The schmatics validator instance

        Raises
        ------
        ValidationError
            If any of the files do not conform to the schema outlines in `otu_schema`

        Notes
        -----
        We assume that the extension dictates the filetype
    """

    _otu_exts = {"tsv": [".tsv", ".txt", ".counts"], "biom": [".biom", ".hdf5"]}
    _meta_exts = [".csv", ".tsv"]
    _tax_exts = [".csv", ".tsv"]

    def __init__(self, dtype: str, ext: Optional[str] = None) -> None:
        self._dtype = dtype
        if dtype not in self._otu_exts.keys():
            raise TypeError(
                f"{dtype} is not supported. Try one of {self._otu_exts.keys()}"
            )
        if ext:
            self._otu_exts[self._dtype].append(ext)
        self.validator = BiomType()

    @property
    def configuration(self) -> Dict[str, Union[str, List[str]]]:
        """
            Dictionary showing the current configuration of the instance

            Returns
            -------
            Dict[str, Union[str, List[str]]]
        """
        return {
            "dtype": self._dtype,
            "valid_otu_ext": self._otu_exts[self._dtype],
            "valid_meta_ext": self._meta_exts,
            "valid_tax_ext": self._tax_exts,
        }

    def _validate_ext(self, fpath: pathlib.Path) -> bool:
        """
            Determines whether the filetype is supported

            Parameters
            ----------
            fpath : pathlib.Path

            Returns
            -------
            bool
        """
        exts = self._otu_exts[self._dtype]
        return bool(fpath.suffix in exts)

    def _load_from_biom(self, otu_file: pathlib.Path) -> Table:
        """
            Read biom table from file

            Parameters
            ----------
            otu_file : pathlib.Path
                The path to the OTU file in `biom` format

            Returns
            -------
            Table
                A `biom.Table` instance containing the OTU, meta, tax data
        """
        otudata = load_table(otu_file)
        self.validator.validate(otudata)
        return otudata

    @staticmethod
    def _extract_data(data_file: pathlib.Path, valid_exts: List[str]) -> pd.DataFrame:
        """
            Extract data as a `pd.DataFrame` from file

            Parameters
            ----------
            data_file : pathlib.Path
                The path to the data file
            valid_exts : List[str]
                A list of valid extensions

            Returns
            -------
            pd.DataFrame
                `pd.DataFrame` created from the data_file
        """
        ext = data_file.suffix
        if ext in valid_exts:
            if ext == "tsv":
                data = pd.read_table(data_file, sep="\t", index_col=0, na_filter=False)
            elif ext == "csv":
                data = pd.read_csv(data_file, sep=",", index_col=0, na_filter=False)
            else:
                data = pd.read_csv(
                    data_file, sep=None, engine="python", index_col=0, na_filter=False
                )
        else:
            raise TypeError(
                "The input metadata file type is not supported. "
                f"Valid extensions are {valid_exts}"
            )
        return data

    def _load_from_tsv(
        self, otu_file: pathlib.Path, meta_file: pathlib.Path, tax_file: pathlib.Path
    ) -> Table:
        """
            Read OTU counts file to biom table and add metadata and taxonomy data

            Parameters
            ----------
            otu_file : pathlib.Path
                The path to the tsv file containing the OTU counts table
            meta_file : pathlib.Path
                The path to the csv file containing the metadata information
            tax_file : pathlib.Path
                The path to the csv file containing the taxonomy information

            Returns
            -------
            Table
                A `biom.Table` instance containing the OTU, meta, tax data
        """
        otudata = load_table(otu_file)
        metadata = self._extract_data(meta_file, self._meta_exts)
        metadata.index = metadata.index.astype(str)
        samplemeta_type = SamplemetaType()
        samplemeta_type.validate(metadata)
        taxdata = self._extract_data(tax_file, self._tax_exts)
        taxdata.index = taxdata.index.astype(str)
        obsmeta_type = ObsmetaType()
        obsmeta_type.validate(taxdata)
        otudata.add_metadata(metadata.to_dict(orient="index"), axis="sample")
        otudata.add_metadata(taxdata.to_dict(orient="index"), axis="observation")
        self.validator.validate(otudata)
        return otudata

    def load_validate(
        self,
        otu_file: pathlib.Path,
        meta_file: Optional[pathlib.Path] = None,
        tax_file: Optional[pathlib.Path] = None,
    ) -> Table:
        """
            Load the data and validate

            Parameters
            ----------
            otu_file : pathlib.Path
                The path to the `OTU` counts table
            meta_file : pathlib.Path, optional
                The path to the sample metadata file
                This argument is required if `dtype` is 'tsv'
            tax_file : pathlib.Path, optional
                The path to the taxonomy file
                This argument is required if `dtype` is 'tsv'

            Returns
            -------
            Table
                `biom.Table` containing all the data
        """
        err_msg = (
            "The input OTU file type is not supported. "
            f"Valid extensions are {self._otu_exts[self._dtype]}"
        )
        if self._dtype == "biom":
            if self._validate_ext(otu_file):
                otu_table = self._load_from_biom(otu_file)
            else:
                raise ValueError(err_msg)
        elif self._dtype == "tsv":
            if meta_file and tax_file:
                if self._validate_ext(otu_file):
                    otu_table = self._load_from_tsv(otu_file, meta_file, tax_file)
                else:
                    raise TypeError(err_msg)
            else:
                raise ValueError("Missing metadata or taxonomy data")
        return otu_table
