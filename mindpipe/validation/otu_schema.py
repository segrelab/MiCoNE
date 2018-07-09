"""
    Module that defines the schema for a valid OTU table

    .. todo::
        1. Define BiomType class - make this a BaseType
        2. Validate OTU counts
        3. Validate whether metadata and taxon data have the correct structure
"""

from itertools import chain
import re

from biom import Table
import numpy as np
from schematics.types import BaseType
from schematics.exceptions import ValidationError


class HeaderType(BaseType):
    """
        DataType that describes the expected structure and format for the sample headers
    """

    def validate_header(self, value):
        """ Check whether the header is valid """
        if any(not isinstance(v, str) for v in value):
            raise ValidationError("Invalid header. All samples must be strings")


class IndexType(BaseType):
    """ DataType that describes the expected structure and format for the OTU indices """

    def validate_index_str(self, value):
        if any(not isinstance(v, str) for v in value):
            raise ValidationError("Invalid index. All indices must be strings")

    def validate_index_unique(self, value):
        if len(value) != len(set(value)):
            raise ValidationError("Invalid index. All indices must be unqiue")


class DataType(BaseType):
    """" DataType that describes the expected structure and format for abundance values """

    def __init__(self, norm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.norm = norm

    def validate_data_npfloat(self, value):
        if not value.dtype == 'float64':
            raise ValidationError("Invalid data. Abundances must be float64")

    def validate_data_range(self, value):
        if value.min('whole') < 0:
            raise ValidationError("Invalid data. Abundances cannot be negative")
        if self.norm:
            if value.max('whole') > 1 or value.min('whole') < 0:
                raise ValidationError("Invalid data. Abundances are not normalized")
            if any(not np.isclose(v, 1.0) for v in value.sum('sample')):
                raise ValidationError("Invalid data. Abundances are not normalized")


# TODO: Implement validation for this BaseType
class SamplemetaType(BaseType):
    """ DataType that describes the expected structure and format for the sample metadata """

    def validate_samplemeta_headers(self, value):
        pass


class ObsmetaType(BaseType):
    """ DataType that describes the expected structure and format for the observation metadata """
    _keys = [
        'kingdom',
        'phylum',
        'class',
        'order',
        'family',
        'genus',
        'species'
    ]

    def validate_obsmeta_headers(self, value):
        for col in value.columns:
            if col not in self._keys:
                raise ValidationError(
                    "Invalid observation metadata. "
                    f"Unknown attribute {col} present"
                )
        for key in self._keys:
            if key not in value.columns:
                raise ValidationError(
                    "Invalid observation metadata. "
                    f"Required attribute {key} not present"
                )

    def validate_obsmeta_data(self, value):
        data_items = chain(*value.values.tolist())
        pattern = re.compile(r'^[a-zA-Z0-9-.]+$')
        for item in data_items:
            cond1 = not item[0].isupper()
            cond2 = not bool(pattern.match(item))
            if cond1 or cond2:
                raise ValidationError(
                    "Invalid observation metadata. "
                    f"Taxonomy names are not standard: {item} is not allowed"
                )


class BiomType(BaseType):
    """
        DataType that describes the expected structure and format for the `biom.Table`

        Parameters
        ----------
        norm : bool, optional
            True if abundances are normalized
            Default value is False
    """

    def __init__(self, norm=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.norm = norm

    def validate_istable(self, value):
        """ Check whether the object is a `biom.Table` """
        if not isinstance(value, Table):
            raise ValidationError("Object must be a `biom.Table` instance")

    def validate_samples(self, value):
        """ Check whether the samples (columns) of the Table are valid """
        header_type = HeaderType()
        header_type.validate(value.ids(axis="sample"))

    def validate_index(self, value):
        """ Check whether the indices in the Table are valid """
        index_type = IndexType()
        index_type.validate(value.ids(axis="observation"))

    def validate_data(self, value):
        """ Check whether the data in the Table is valid """
        data_type = DataType(self.norm)
        data_type.validate(value)

    def validate_sample_metadata(self, value):
        """ Check whether the sample metadata in the Table is valid """
        samplemeta_type = SamplemetaType()
        sample_metadata = value.metadata_to_dataframe('sample')
        samplemeta_type.validate(sample_metadata)

    def validate_obs_metadata(self, value):
        """ Check whether the observation metadata in the Table is valid """
        obsmeta_type = ObsmetaType()
        obs_metadata = value.metadata_to_dataframe('observation')
        obsmeta_type.validate(obs_metadata)
