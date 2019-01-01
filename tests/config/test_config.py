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
        config_folder = pipeline_settings["config_folder"]
        assert Config(config_folder)
