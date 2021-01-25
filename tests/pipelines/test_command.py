"""
    Module containing tests for the `Command` class
"""

import os

import pytest

from micone.pipelines import Command
from micone.logging import LOG


class TestCommand:
    """ Tests for the `Command` class """

    def test_init(self):
        cmd = "ls"
        profile = "local"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        assert command.run()

    def test_output(self):
        cmd = "uname"
        profile = "local"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        with pytest.raises(NotImplementedError):
            command.output
        command.run()
        output = command.output
        assert output == "Linux\n"

    def test_error(self):
        cmd = "random_command"
        profile = "local"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        with pytest.raises(FileNotFoundError):
            command.run()
        cmd = "ls &&"
        command = Command(cmd, profile, timeout)
        command.run()
        error = command.error
        assert error == "ls: cannot access '&&': No such file or directory\n"

    def test_log(self, tmpdir):
        cmd = "ls"
        profile = "local"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        command.run()
        command.log()
        assert os.path.exists(LOG.path)

    def test_profile(self):
        cmd = "ls"
        profile = "sge"
        timeout = 1000
        with pytest.raises(ValueError):
            command = Command(cmd, profile, timeout)
        project = "project"
        command = Command(cmd, profile, timeout, project=project)
        assert command.cmd.startswith("qsub ")
