"""
    Module that defines the `Otu` objects and methods to manipulate it
"""

import pathlib
from typing import Optional

from biom import Table
import pandas as pd

from ..validation import OtuValidator, BiomType, SamplemetaType, ObsmetaType


class Otu:
    """
        An object that represents the OTU counts table

        Parameters
        ----------
        otu_data : Table
            `biom.Table` object containing OTU data
        sample_metadata : pd.DataFrame, optional
            `pd.DataFrame` containing metadata for the samples
        obs_metadata : pd.DataFrame,  optional
            `pd.DataFrame` containing metadata for the observations (OTUs)

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
            otu_data: Table,
            sample_metadata: Optional[pd.DataFrame] = None,
            obs_metadata: Optional[pd.DataFrame] = None
    ) -> None:
        biom_type = BiomType()
        biom_type.validate(otu_data)
        self.otu_data = otu_data.copy()
        if sample_metadata:
            samplemeta_type = SamplemetaType()
            samplemeta_type.validate(sample_metadata)
            self.otu_data.add_metadata(sample_metadata.to_dict(orient="index"), axis="sample")
        if obs_metadata:
            obsmeta_type = ObsmetaType()
            obsmeta_type.validate(obs_metadata)
            self.otu_data.add_metadata(obs_metadata.to_dict(orient="index"), axis="observation")
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
