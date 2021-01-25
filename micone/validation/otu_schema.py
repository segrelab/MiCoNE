"""
    Module that defines the schema for a valid OTU table
"""

from biom import Table
import numpy as np
from schematics.exceptions import ValidationError
from schematics.types import BaseType


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
        if not value.dtype == "float64":
            raise ValidationError("Invalid data. Abundances must be float64")

    def validate_data_range(self, value):
        df = value.to_dataframe(dense=True)
        if df.values.min() < 0:
            raise ValidationError("Invalid data. Abundances cannot be negative")
        if self.norm:
            if df.values.max() > 1 or df.values.min() < 0:
                raise ValidationError("Invalid data. Abundances are not normalized")
            if any(not np.isclose(v, 1.0) for v in df.values.sum(axis=0)):
                raise ValidationError("Invalid data. Abundances are not normalized")


class SamplemetaType(BaseType):
    """ DataType that describes the expected structure and format for the sample metadata """

    def validate_samplemeta_columns(self, value):
        if len(value.columns) < 1:
            raise ValidationError("Invalid columns in sample metdata")

    def validate_samplemeta_index(self, value):
        if len(value.index) != len(set(value.index)):
            raise ValidationError(
                "Invalid index in sample metadata. All indices must be unqiue"
            )

    def validate_structure(self, value):
        if any(not isinstance(v, str) for v in value.index):
            raise ValidationError("Invalid index. All indices must be strings")
        if value.index.str.startswith("#").any():
            raise ValidationError(
                "Invalid sample metadata structure. Possibly incorrect header"
            )


class ObsmetaType(BaseType):
    """ DataType that describes the expected structure and format for the observation metadata """

    _req_keys = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    _extra_keys = ["Confidence", "Abundance"]

    def validate_index(self, value):
        if any(not isinstance(v, str) for v in value.index):
            raise ValidationError("Invalid index. All indices must be strings")

    def validate_obsmeta_headers(self, value):
        for col in value.columns:
            if col not in self._req_keys and col not in self._extra_keys:
                raise ValidationError(
                    f"Invalid observation metadata. Unknown attribute {col} present"
                )
        # Check if keys are in order
        # i.e. if genus is present everything above that level is present
        for key in self._req_keys:
            if key not in value.columns:
                ind = self._req_keys.index(key)
                if len(value.columns) != ind:
                    raise ValidationError(
                        f"Invalid observation metadata. Required attribute {key} not present"
                    )
                else:
                    break

    def validate_obsmeta_data(self, value):
        if self._extra_keys[0] in value.columns:
            confidence = value[self._extra_keys[0]]
            if confidence.dtype == float:
                cond1 = 0 <= confidence.min() <= 1
                cond2 = 0 <= confidence.max() <= 1
                if not cond1 and not cond2:
                    raise ValidationError(
                        "Invalid observation metadata. "
                        f"{self._extra_keys[0]} must have a value between 0 and 1"
                    )
            else:
                raise ValidationError(
                    "Invalid observation metadata. "
                    f"{self._extra_keys[0]} column must be of type float"
                )
            df = value.drop(self._extra_keys[0], axis=1)
        else:
            df = value
        if self._extra_keys[1] in value.columns:
            abundance = value[self._extra_keys[1]]
            if abundance.dtype != float:
                raise ValidationError(
                    "Invalid observation metadata. "
                    f"{self._extra_keys[1]} column must be of type float"
                )
            df = value.drop(self._extra_keys[1], axis=1)
        else:
            df = value
        for level, data in df.items():
            filt_data = data[data != ""]
            if level == "Species":
                query = filt_data[
                    ~filt_data.str.contains(r"^[a-zA-Z0-9-._ ]+(?<! )$")
                ].any()
                # TODO: FIXME:
                # if query:
                #     raise ValidationError(
                #         "Invalid observation metadata. "
                #         f"Taxonomy names are not standard: {query} is not allowed in {level}"
                #     )
            elif level in ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus"]:
                query = filt_data[
                    ~filt_data.str.contains(r"^[a-zA-Z0-9-._ ]+(?<! )$")
                ].any()
                # TODO: FIXME:
                # if query:
                #     raise ValidationError(
                #         "Invalid observation metadata. "
                #         f"Taxonomy names are not standard: {query} is not allowed in {level}"
                #     )


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
        sample_metadata = value.metadata_to_dataframe("sample")
        samplemeta_type.validate(sample_metadata)

    def validate_obs_metadata(self, value):
        """ Check whether the observation metadata in the Table is valid """
        obsmeta_type = ObsmetaType()
        obs_metadata = value.metadata_to_dataframe("observation")
        obsmeta_type.validate(obs_metadata)
