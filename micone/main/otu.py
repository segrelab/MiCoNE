"""
    Module that defines the `Otu` objects and methods to manipulate it
"""

import json
import pathlib
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Tuple

from biom import Table
from biom.util import biom_open
import numpy as np
import pandas as pd

from ..validation import OtuValidator, BiomType, SamplemetaType, ObsmetaType
from .lineage import Lineage


Filterfun = Callable[[np.ndarray, str, dict], bool]
Hashfun = Callable[[str, dict], Hashable]


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
    tax_level : str
        The taxonomy level of the current Otu instance

    Notes
    -----
    All methods that manipulate the Otu object return new objects
    """

    def __init__(
        self,
        otu_data: Table,
        sample_metadata: Optional[pd.DataFrame] = None,
        obs_metadata: Optional[pd.DataFrame] = None,
    ) -> None:
        if not isinstance(otu_data, Table):
            raise TypeError("Otu data must be of type `biom.Table`")
        otu_data_copy = otu_data.copy()
        if sample_metadata is not None:
            samplemeta_type = SamplemetaType()
            samplemeta_type.validate(sample_metadata)
            otu_data_copy.add_metadata(
                sample_metadata.to_dict(orient="index"), axis="sample"
            )
        if obs_metadata is not None:
            obsmeta_type = ObsmetaType()
            obsmeta_type.validate(obs_metadata)
            otu_data_copy.add_metadata(
                obs_metadata.to_dict(orient="index"), axis="observation"
            )
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
        return self.otu_data.metadata_to_dataframe("sample")

    @property
    def obs_metadata(self) -> pd.DataFrame:
        """ Lineage data for the observations (OTUs) """
        obs_metadata = self.otu_data.metadata_to_dataframe("observation")
        lineage = list(Lineage._fields)
        n_tax_levels = len(set(obs_metadata.columns) & set(lineage))
        lineage_columns = lineage[:n_tax_levels]
        extra_columns = list(set(obs_metadata.columns) - set(lineage_columns))
        if extra_columns:
            columns: List[str] = lineage_columns + extra_columns
        else:
            columns = lineage_columns
        return obs_metadata[columns]

    @property
    def tax_level(self) -> str:
        """
        Returns the taxonomy level of the Otu instance

        Returns
        -------
        str
            The lowest taxonomy defined in the Otu instance
        """
        obs_metadata = self.otu_data.metadata_to_dataframe("observation")
        lineage = list(Lineage._fields)
        n_tax_levels = len(set(obs_metadata.columns) & set(lineage))
        return Lineage._fields[n_tax_levels - 1]

    def filter(
        self,
        ids: Optional[Iterable[str]] = None,
        func: Optional[Filterfun] = None,
        axis: str = "observation",
    ) -> "Otu":
        """
        Filter Otu instance based on ids or func

        Parameters
        ----------
        ids : Iterable[str], optional
            An iterable of ids to keep.
            If ids are not supplied then func must be supplied
        func : Callable[[np.ndarray, str, dict], bool], optional
            A function that takes in (values, id_, md) and returns a bool
            If func is not supplied then ids must be supplied
            If both ids and func are supplied then ids are used
        axis : {'sample', 'observation'}, optional
            The axis along which to filter the Otu instance
            Default value is 'observation'

        Returns
        -------
        Otu
            Filtered Otu instance
        """
        if ids is not None:
            otu_filtered = self.otu_data.filter(ids, inplace=False, axis=axis)
        elif func:
            otu_filtered = self.otu_data.filter(func, inplace=False, axis=axis)
        else:
            raise TypeError("Either ids or func must be supplied")
        return Otu(otu_filtered)

    def normalize(self, axis: str = "sample", method: str = "norm") -> "Otu":
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
        if method == "norm":
            norm_otu = self.otu_data.norm(axis=axis, inplace=False)
        elif method == "rarefy":
            raise NotImplementedError("This method is not implemented yet")
        elif method == "css":
            raise NotImplementedError("This method is not implemented yet")
        else:
            raise ValueError(
                "Invalid method. Supported methods are {'norm', 'rarefy', 'css'}"
            )
        return Otu(norm_otu)

    def is_norm(self, axis: str = "sample") -> bool:
        """
        Returns true if the Otu instance has been normalized
        """
        otu_data = self.otu_data.to_dataframe()
        if axis == "sample":
            return bool(np.isclose(otu_data.sum(axis=0), 1.0).all())
        if axis == "observation":
            return bool(np.isclose(otu_data.sum(axis=1), 1.0).all())
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
            raise ValueError(
                "Otu instance is normalized and hence will not work with this method"
            )
        filt_fun = lambda val, *_: round(val.sum()) >= count_thres
        new_otu = self.otu_data.filter(filt_fun, axis="sample", inplace=False)
        return Otu(new_otu)

    def rm_sparse_obs(
        self, prevalence_thres: float = 0.05, abundance_thres: float = 0.01
    ) -> "Otu":
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
        filt_fun = (
            lambda val, *_: (val.astype(int).astype(bool).mean()) >= prevalence_thres
        )
        otu_dense_obs = self.otu_data.filter(
            filt_fun, axis="observation", inplace=False
        )
        otu_df = otu_dense_obs.to_dataframe()
        if otu_df.apply(pd.api.types.is_sparse).any():
            otu_rel_abund = (otu_df / otu_df.sum(axis=0)).sparse.to_dense()
        else:
            otu_rel_abund = otu_df / otu_df.sum(axis=0)
        ind_above_thres = otu_rel_abund.index[
            (otu_rel_abund > abundance_thres).any(axis=1)
        ]
        new_otu = self.otu_data.filter(
            ind_above_thres, axis="observation", inplace=False
        )
        ind_below_thres = set(self.otu_data.ids("observation")) - set(ind_above_thres)
        otu_sparse_obs = self.otu_data.filter(
            ind_below_thres, axis="observation", inplace=False
        )
        new_row = Table(
            otu_sparse_obs.sum(axis="sample"),
            ["otu_merged"],
            self.otu_data.ids(axis="sample"),
        )
        tax_level = self.tax_level
        random_row_metadata = dict(self.otu_data.metadata(axis="observation")[0])
        new_row.add_metadata(
            {
                "otu_merged": {
                    **random_row_metadata,
                    **Lineage("Unclassified").to_dict(tax_level),
                }
            },
            axis="observation",
        )
        final_otu = new_otu.concat([new_row], axis="observation")
        return Otu(final_otu)

    def partition(self, axis: str, func: Hashfun) -> Iterable[Tuple[str, "Otu"]]:
        """
        Partition the Otu instance based on the func and axis

        Parameters
        ----------
        axis : str
            The axis on which to partition
        func : Callable[[str, dict], Hashable]
            The function that takes in (id, metadata) and returns a hashable

        Returns
        -------
        Iterable[Tuple[str, Otu]]
            An iterable of tuples - ('label', Otu)

        Notes
        -----
        1. To group by lineage "level" use:
            func = lambda id_, md: Lineage(**md).get_superset(level)
        """
        if axis == "observation" and self.is_norm(axis="sample"):
            raise ValueError(
                "Cannot partition sample normalized Otu instance on observation"
            )
        if axis == "sample" and self.is_norm(axis="observation"):
            raise ValueError(
                "Cannot partition observation normalized Otu instance on sample"
            )
        partitions = self.otu_data.partition(func, axis=axis)
        for label, table in partitions:
            yield label, Otu(table)

    def collapse_taxa(self, level: str) -> Tuple["Otu", Dict[str, List[str]]]:
        """
        Collapse Otu instance based on taxa

        Parameters
        ----------
        level : str
            The tax level of the collapsed table
            This will also be used as the prefix for the unique ids

        Returns
        -------
        Tuple[Otu, dict]
            Collapsed Otu instance
        """
        obs_metadata_cols = list(self.obs_metadata)
        lineage_cols = list(Lineage._fields)
        unwanted_obs_metadata_cols = list(set(obs_metadata_cols) - set(lineage_cols))
        otu_data_copy = self.otu_data.copy()
        otu_data_copy.del_metadata(keys=unwanted_obs_metadata_cols, axis="observation")
        obs_metadata_copy = self.obs_metadata.drop(unwanted_obs_metadata_cols, axis=1)
        if level not in Lineage._fields:
            raise ValueError(f"level must be one of {Lineage._fields}")
        cfunc = lambda id_, md: str(Lineage(**md).get_superset(level))
        otu_collapse = otu_data_copy.collapse(
            cfunc, axis="observation", norm=False, include_collapsed_metadata=True
        )
        curr_ids = otu_collapse.ids(axis="observation")
        children_group_list = [
            i["collapsed_ids"] for i in otu_collapse.metadata(axis="observation")
        ]
        children_groups = dict(zip(curr_ids, children_group_list))
        otu_collapse.del_metadata(axis="observation")
        afunc = lambda x: pd.Series(
            Lineage(**x.to_dict()).get_superset(level).to_dict(level)
        )
        obs_collapse = obs_metadata_copy.apply(afunc, axis=1)
        gfunc = lambda x: str(Lineage(**x.to_dict()))
        obs_collapse.index = obs_collapse.apply(gfunc, axis=1)
        obs_collapse.drop_duplicates(inplace=True)
        otu_collapse.add_metadata(
            obs_collapse.to_dict(orient="index"), axis="observation"
        )
        obs_dict = json.loads(
            otu_collapse.metadata_to_dataframe("observation").to_json(orient="split")
        )
        unq_id_map = {k: f"{level}_{i}" for i, k in enumerate(curr_ids)}
        obs_ids = [unq_id_map[i] for i in obs_dict["index"]]  # get ordered unique ids
        children_dict = {unq_id_map[k]: v for k, v in children_groups.items()}
        sample_ids = otu_collapse.ids(axis="sample")
        observation_metadata = otu_collapse.metadata_to_dataframe(
            axis="observation"
        ).to_dict(orient="records")
        sample_metadata = otu_collapse.metadata_to_dataframe(axis="sample").to_dict(
            orient="records"
        )
        new_table = Table(
            otu_collapse.matrix_data,
            obs_ids,
            sample_ids,
            observation_metadata=observation_metadata,
            sample_metadata=sample_metadata,
        )
        return Otu(new_table), children_dict

    def write(
        self, base_name: str, fol_path: str = "", file_type: str = "biom"
    ) -> None:
        """
        Write Otu instance object to required file_type

        Parameters
        ----------
        base_name : str
            The base name without extension to be used for the files
        fol_path : str, optional
            The folder where the files are to be written
            Default is current directory
        file_type : {'tsv', 'biom'}, optional
            The type of file data is to be written to
            Default is 'biom'
        """
        folder = pathlib.Path(fol_path)
        if not folder.exists():
            folder.mkdir()
        if file_type == "biom":
            fname = base_name + ".biom"
            fpath = str(folder / fname)
            with biom_open(fpath, "w") as fid:
                self.otu_data.to_hdf5(fid, "Constructed using micone")
        elif file_type == "tsv":
            otu_name = base_name + "_otu.tsv"
            otu_path = folder / otu_name
            with open(otu_path, "w") as fid:
                # NOTE: delete header comment from output
                data = self.otu_data.to_tsv().split("\n", 1)[-1]
                fid.write(data)
            sample_metadata_name = base_name + "_sample_metadata.tsv"
            sample_metadata_path = folder / sample_metadata_name
            self.sample_metadata.to_csv(sample_metadata_path, sep="\t", index=True)
            obs_metadata_name = base_name + "_obs_metadata.csv"
            obs_metadata_path = folder / obs_metadata_name
            self.obs_metadata.to_csv(obs_metadata_path, index=True)
        else:
            raise ValueError("Supported file types are 'tsv' and 'biom'")
