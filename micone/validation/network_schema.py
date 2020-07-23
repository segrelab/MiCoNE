"""
    Module that defines the schema for interactions, pvalues, networks and their metadata
"""

import numpy as np
import pandas as pd
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import (
    BaseType,
    DateType,
    DictType,
    FloatType,
    IntType,
    ListType,
    ModelType,
    StringType,
    UnionType,
)


class InteractionmatrixType(BaseType):
    """
        DataType that describes the expected structure of an interaction matrix

        Parameters
        ----------
        symm : bool, optional
            True if interaction matrix is expected to be symmetric
            Default value is False
    """

    def __init__(self, symm=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symm = symm

    def validate_isdataframe(self, value):
        """ Check whether the object is a pandas DataFrame """
        if not isinstance(value, pd.DataFrame):
            raise ValidationError(
                "Interaction matrix must be a `pd.DataFrame` instance"
            )

    def validate_headers(self, value):
        """ Check whether the rows and columns are the same """
        if len(value.index) != len(value.columns):
            raise ValidationError(
                "Interaction matrix must have same number of rows and columns"
            )
        if any(value.index != value.columns):
            raise ValidationError(
                "Row and column header of an interaction matrix should match"
            )

    def validate_symmetry(self, value):
        """ Check whether the the interaction matrix is symmetric """
        if self.symm:
            if value.shape[0] != value.shape[1]:
                raise ValidationError("Interaction matrix is not symmetric")
            if not np.allclose(value, value.T):
                raise ValidationError("Interaction matrix is not symmetric")

    def validate_data(self, value):
        if not value.values.dtype == float and not value.values.dtype == int:
            raise ValidationError("Invalid data. Interactions must be int or float")


class CorrelationmatrixType(InteractionmatrixType):
    """ DataType that describes the expected structure of a correlation matrix """

    def __init__(self, *args, **kwargs):
        super().__init__(symm=True, *args, **kwargs)

    def validate_data_range(self, value):
        if value.values.max() > 1 or value.values.min() < -1:
            raise ValidationError("Correlation matrix must be bound by -1 and 1")


class PvaluematrixType(InteractionmatrixType):
    """ DataType that describes the expected structure of a pvalue matrix """

    def validate_data_range(self, value):
        if value.values.max() > 1 or value.values.min() < 0:
            raise ValidationError("Pvalue matrix must be bound by 0 and 1")


class PublicationModel(Model):
    """ Model that describes the expected structure of the publication input """

    date = DateType(required=True)
    authors = ListType(DictType(StringType), required=True)
    pubmed_id = StringType(required=True)


class MetadataModel(Model):
    """ Model that describes the expected structure of the network metadata input """

    host = StringType(required=True)
    condition = StringType(required=True)
    location = StringType(required=True)
    experimental_metadata = DictType(StringType, required=True)
    publication = ModelType(PublicationModel, required=True)
    description = StringType(required=True)


class ChildrenmapType(BaseType):
    """ DataType that describes the expected structure of the children map dictionary """

    def validate_keys(self, value):
        for k in value.keys():
            if not isinstance(k, str):
                raise ValidationError("Children map must have string keys")

    def validate_values(self, value):
        for v in value.values():
            if not isinstance(v, list):
                raise ValidationError(
                    "Children map must have lists of strings as values"
                )
            for elem in v:
                if not isinstance(elem, str):
                    raise ValidationError(
                        "Children map must have lists of strings as values"
                    )


class NodeModel(Model):
    """ Model that describes the structure of one node in the network """

    id = StringType(min_length=2, required=True)
    lineage = StringType(required=True)
    name = StringType(required=True)
    taxid = IntType(required=True)
    taxlevel = StringType(
        regex=r"(Kingdom|Phylum|Class|Order|Family|Genus|Species)", required=True
    )
    abundance = FloatType()
    children = ListType(StringType, required=True)


class NodesModel(Model):
    """ Model that describes the structure of the nodes in the network """

    nodes = ListType(ModelType(NodeModel), required=True)


class LinkModel(Model):
    """ Model that describes the structure of one link in the network """

    pvalue = FloatType()
    weight = FloatType(required=True)
    source = StringType(min_length=2, required=True)
    target = StringType(min_length=2, required=True)


class LinksModel(Model):
    """ Model that describes the structure of one link in the network """

    links = ListType(ModelType(LinkModel), required=True)


class NetworkmetadataModel(MetadataModel):
    """ Model that describes the expected structure of the network metadata """

    computational_metadata = DictType(
        UnionType(types=(StringType, FloatType)), required=True
    )
    directionality = StringType(regex=r"(undirected|directed)", required=True)
    interaction_type = StringType()


class ElistType(BaseType):
    """ DataType that describes the expected structure of an edge list """

    def validate_headers_index(self, value):
        if "source" not in value.columns:
            raise ValidationError("source column must be present in the edge list")
        if "target" not in value.columns:
            raise ValidationError("target column must be present in the edge list")
        if "weight" not in value.columns:
            raise ValidationError("weight column must be present in the edge list")
        if len(value["source"]) == len(set(value["source"])):
            raise ValidationError("Duplicate entries in source column not allowed")
        if len(value["target"]) == len(set(value["target"])):
            raise ValidationError("Duplicate entries in target column not allowed")
