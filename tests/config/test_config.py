"""
    Module containing tests for the Config class
"""

import pytest

from mindpipe.config import Config


class TestConfig:
    """ Tests for the Config class """

    def test_init(self):
        assert Config()
