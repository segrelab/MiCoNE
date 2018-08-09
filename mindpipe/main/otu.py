"""
    Module that defines the `Otu` objects and methods to manipulate it
"""

import pathlib
from typing import Optional

import pandas as pd

from ..validation import OtuValidator


class Otu:
    """
        An object that represents the OTU counts table

        Parameters
        ----------
        otu_file : str
            The path to the `OTU` counts file
        meta_file : str, optional
            The path to the sample metadata file
        tax_file : str, optional
            The path to the taxonomy file
        dtype : {'biom', 'tsv'}
            The type of OTU file that is input
        ext : str, optional
            The extension of the file if other than supported extensions
            Supported extensions:
            - 'tsv' dtype: 'tsv', 'txt', 'counts'
            - 'biom' dtype: 'biom', 'hdf5'

        Attributes
        ----------
        otu_data : biom.Table
            OTU counts table in the `biom.Table` format
        sample_metadata : pd.DataFrame
            Metadata for the samples
        obs_metadata :  pd.DataFrame
            Lineage data for the observations (OTUs)
    """

    def __init__(
            self,
            otu_file: str,
            meta_file: Optional[str] = None,
            tax_file: Optional[str] = None,
            dtype: str = "biom",
            ext: Optional[str] = None,
    ) -> None:
        otu_validator = OtuValidator(dtype=dtype, ext=ext)
        otu_path = pathlib.Path(otu_file)
        if otu_path.exists():
            meta_path = pathlib.Path(meta_file) if meta_file else meta_file
            tax_path = pathlib.Path(tax_file) if tax_file else tax_file
            self.otu_data = otu_validator.load_validate(otu_path, meta_path, tax_path)
        else:
            raise FileNotFoundError("Missing input files")

    @property
    def sample_metadata(self) -> pd.DataFrame:
        """
            Metadata for the samples

            Returns
            -------
            pd.DataFrame
        """
        return self.otu_data.metadata_to_dataframe('sample')

    @property
    def obs_metadata(self) -> pd.DataFrame:
        """
            Lineage data for the observations (OTUs)

            Returns
            -------
            pd.DataFrame
        """
        return self.otu_data.metadata_to_dataframe('observation')
