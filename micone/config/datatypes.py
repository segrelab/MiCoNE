"""
    Module to store pipeline datatypes
"""

import collections
from typing import Dict, Iterator, List, Set, Tuple, Union


class DataType(collections.Hashable):
    """
        The class that stores a datatype of the pipeline constructor

        Parameters
        ----------
        data : Dict[str, Any]
            The information about a particular datatype

        Attributes
        ----------
        name : str
            DataType name
        desc : str
            DataType description
        format : Set[str]
            DataType allowed formats
    """

    def __init__(self, data: Tuple[str, Dict[str, Union[str, List[str]]]]) -> None:
        if len(data) != 2:
            raise ValueError(f"Invalid DataType {data}")
        key, value = data
        if "desc" not in value or "format" not in value:
            raise ValueError(f"Invalid DataType {data}")
        self.name = key
        if isinstance(value["desc"], str):
            self.desc = value["desc"]
        else:
            raise TypeError(f"Invalid DataType {data}. Description has to be a string.")
        if isinstance(value["format"], list):
            self.format = set(value["format"])
        else:
            raise TypeError(
                f"Invalid DataType {data}. Format has to be a list of strings."
            )

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if self.name != other.name:
            return False
        if self.desc != other.desc:
            return False
        if self.format != other.format:
            return False
        return True

    def __repr__(self) -> str:
        return f"<DataType name={self.name} desc={self.desc} format={self.format}>"

    def __str__(self) -> str:
        return self.name


class DataTypes(collections.Set):
    """
        The set of all datatypes supported by the pipeline constructor

        Parameters
        ----------
        data : Dict[str, Dict[str, Any]]
            A dictionary containing information about the pipeline datatypes
    """

    def __init__(self, data: Dict[str, Dict[str, Union[str, List[str]]]]) -> None:
        self.dtypes: Set[DataType] = set()
        for key, value in data.items():
            data_type = DataType((key, value))
            if data_type in self.dtypes:
                raise ValueError("Duplicate DataTypes detected in settings. Aborting")
            self.dtypes.add(data_type)

    def __iter__(self) -> Iterator:
        return iter(self.dtypes)

    def __len__(self) -> int:
        return len(self.dtypes)

    def __contains__(self, value: str) -> bool:
        return value in [dtype.name for dtype in self.dtypes]

    def __getitem__(self, key: str) -> DataType:
        for dtype in self.dtypes:
            if dtype.name == key:
                return dtype
        raise KeyError(f"{key} is not in DataTypes")

    def __repr__(self) -> str:
        dtypes = [dtype.name for dtype in self.dtypes]
        return f"<DataTypes n={len(self)} dtypes={dtypes}>"
