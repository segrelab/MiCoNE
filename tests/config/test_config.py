"""
    Module containing tests for the Config class
"""

import pytest
import toml

from mindpipe.config import Config


@pytest.mark.usefixtures("pipeline_settings")
class TestConfig:
    """ Tests for the Config class """

    def test_init(self):
        assert Config()

    def test_integrity(self, tmpdir, pipeline_settings):
        file = tmpdir.mkdir("test_config_integrity").join("datatypes.toml")
        datatypes_raw = pipeline_settings["datatypes"]
        missing_datatype = dict(datatypes_raw)
        del missing_datatype["otu_table"]
        with open(file, "w") as fid:
            toml.dump(missing_datatype, fid)
        with pytest.raises(ValueError):
            assert Config(datatypes_file=file)
        wrong_formats = dict(datatypes_raw)
        wrong_formats["otu_table"]["format"] = [".out"]
        with open(file, "w") as fid:
            toml.dump(wrong_formats, fid)
        with pytest.raises(ValueError):
            assert Config(datatypes_file=file)
