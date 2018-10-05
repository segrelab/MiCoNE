"""
    Module containing tests for the DataTypes class
"""

import pytest

from mindpipe.config import DataTypes
from mindpipe.config.datatypes import DataType


@pytest.mark.usefixtures("pipeline_settings")
class TestDataTypes:
    """ Tests for DataTypes class """

    def test_init(self, pipeline_settings):
        raw_data = pipeline_settings["datatypes"]
        assert DataTypes(raw_data)
        wrong_data = {
            "barcode": "code",
            "artifact": {
                "desc": "artifact description",
                "format": ["artifact format"]
            }
        }
        with pytest.raises(ValueError):
            DataTypes(wrong_data)
        wrong_types = {
            "barcode": {
                "desc": 123,
                "format": "format1"
            },
        }
        with pytest.raises(TypeError):
            DataTypes(wrong_types)

    def test_iter_len(self, pipeline_settings):
        raw_data = pipeline_settings["datatypes"]
        data_types = DataTypes(raw_data)
        assert len(data_types) == len(raw_data)
        for dtype in data_types:
            assert isinstance(dtype, DataType)

    def test_contains_getitem(self, pipeline_settings):
        raw_data = pipeline_settings["datatypes"]
        data_types = DataTypes(raw_data)
        test_key = list(raw_data.keys())[0]
        test_value = raw_data[test_key]
        real_dtype = DataType((test_key, test_value))
        assert test_key in data_types
        assert data_types[test_key] == real_dtype
