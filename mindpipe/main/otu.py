"""
    Module that defines the `Otu` objects and methods to manipulate it
"""

import pathlib
from typing import Optional

from biom import Table
import numpy as np
import pandas as pd

from ..validation import OtuValidator, BiomType, SamplemetaType, ObsmetaType
from .lineage import Lineage


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

        Notes
        -----
        All methods that manipulate the Otu object return new objects
    """

    def __init__(
            self,
            otu_data: Table,
            sample_metadata: Optional[pd.DataFrame] = None,
            obs_metadata: Optional[pd.DataFrame] = None
    ) -> None:
        if not isinstance(otu_data, Table):
            raise TypeError("Otu data must be of type `biom.Table`")
        otu_data_copy = otu_data.copy()
        if sample_metadata:
            samplemeta_type = SamplemetaType()
            samplemeta_type.validate(sample_metadata)
            otu_data_copy.add_metadata(sample_metadata.to_dict(orient="index"), axis="sample")
        if obs_metadata:
            obsmeta_type = ObsmetaType()
            obsmeta_type.validate(obs_metadata)
            otu_data_copy.add_metadata(obs_metadata.to_dict(orient="index"), axis="observation")
        biom_type = BiomType()
        biom_type.validate(otu_data_copy)
        self.otu_data = otu_data_copy

    def __repr__(self) -> str:
        n_obs, n_samples = self.otu_data.shape
        return f"<Otu {n_obs}obs x {n_samples}samples>"

    @classmethod
    def load_data(
            cls,
            otu_file: str,
            meta_file: Optional[str] = None,
            tax_file: Optional[str] = None,
            dtype: str = "biom",
            ext: Optional[str] = None,
    ) -> "Otu":
        """
            Load data from files into the `Otu` class instance

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

            Returns
            -------
            Otu
                An instance of the `Otu` class
        """
        otu_validator = OtuValidator(dtype=dtype, ext=ext)
        otu_path = pathlib.Path(otu_file)
        if otu_path.exists():
            meta_path = pathlib.Path(meta_file) if meta_file else meta_file
            tax_path = pathlib.Path(tax_file) if tax_file else tax_file
            otu_data = otu_validator.load_validate(otu_path, meta_path, tax_path)
        else:
            raise FileNotFoundError("Missing input files")
        return cls(otu_data)

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

    @property
    def tax_level(self) -> str:
        """
            Returns the taxonomy level of the Otu instance

            Returns
            -------
            str
                The lowest taxonomy defined in the Otu instance
        """
        n_tax_levels = len(self.obs_metadata.columns)
        return Lineage._fields[n_tax_levels - 1]

    def normalize(self, axis: str = 'sample', method: str = 'norm') -> "Otu":
        """
            Normalize the OTU table along the provided axis

            Parameters
            ----------
            axis : {'sample', 'observation'}, optional
                Axis along which to normalize the OTU table
                Default is 'sample'
            method: {'norm', 'rarefy', 'css'}
                Normalization method to use

            Returns
            -------
            Otu
                Otu instance which is normalized along the given axis
        """
        if method == 'norm':
            norm_otu = self.otu_data.norm(axis=axis, inplace=False)
        elif method == 'rarefy':
            raise NotImplementedError("This method is not implemented yet")
        elif method == 'css':
            raise NotImplementedError("This method is not implemented yet")
        else:
            raise ValueError("Invalid method. Supported methods are {'norm', 'rarefy', 'css'}")
        return Otu(norm_otu)

    def is_norm(self, axis: str = 'sample') -> bool:
        """
            Returns true if the Otu instance has been normalized
        """
        df = self.otu_data.to_dataframe()
        if axis == 'sample':
            return bool(np.isclose(df.sum(axis=0), 1.0).all())
        if axis == 'observation':
            return bool(np.isclose(df.sum(axis=1), 1.0).all())
        raise ValueError("Axis must of either {'sample' or 'observation'}")

    def rm_sparse_samples(self, count_thres: int = 500) -> "Otu":
        """
            Remove samples with read counts less than `count_thres`

            Parameters
            ----------
            count_thres : int, optional
                Counts threshold below which samples are rejected
                Default value is 500

            Returns
            -------
            Otu
                Otu instance with low count samples removed

            Raises
            ------
            ValueError
                If Otu instance is normalized
        """
        if self.is_norm():
            raise ValueError("Otu instance is normalized and hence will not work with this method")
        filt_fun = lambda val, *_: round(val.sum()) >= count_thres
        new_otu = self.otu_data.filter(filt_fun, axis="sample", inplace=False)
        return Otu(new_otu)

    def rm_sparse_obs(self, prevalence_thres: float = 0.05, abundance_thres: float = 0.01) -> "Otu":
        """
            Remove observations with prevalence < `prevalence_thres` and abundance < `abundance_thres`

            Parameters
            ----------
            prevalence_thres : float
                Minimum fraction of samples the observation must be present in in order to be accepted
            abundance_thres : float
                Minimum observation count fraction in a sample needed in order to be accepted

            Returns
            -------
            Otu
                Otu instance with bad observations removed
        """
        filt_fun = lambda val, *_: (val.astype(int).astype(bool).mean()) >= prevalence_thres
        otu_dense_obs = self.otu_data.filter(filt_fun, axis="observation", inplace=False)
        otu_df = otu_dense_obs.to_dataframe()
        otu_rel_abund = (otu_df / otu_df.sum(axis=0)).to_dense()
        ind_above_thres = otu_rel_abund.index[(otu_rel_abund > abundance_thres).any(axis=1)]
        new_otu = self.otu_data.filter(ind_above_thres, axis="observation", inplace=False)
        ind_below_thres = set(self.otu_data.ids("observation")) - set(ind_above_thres)
        otu_sparse_obs = self.otu_data.filter(ind_below_thres, axis="observation", inplace=False)
        new_row = Table(
            otu_sparse_obs.sum(axis="sample"),
            ['otu_merged'],
            self.otu_data.ids(axis="sample")
        )
        tax_level = self.tax_level
        new_row.add_metadata(
            {'otu_merged': Lineage("Unclassified").to_dict(tax_level)},
            axis='observation'
        )
        final_otu = new_otu.concat([new_row], axis="observation")
        return Otu(final_otu)
