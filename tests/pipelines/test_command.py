"""
    Module containing tests for the `Command` class
"""

import os

import pytest

from mindpipe.pipelines import Command


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
        command.run()
        error = command.error
        print(error)
        assert error == "/bin/sh: random_command: command not found\n"

    def test_log(self, tmpdir):
        cmd = "ls"
        profile = "local"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        command.run()
        log_file = tmpdir.mkdir("test_command_log").join("log.txt")
        assert not os.path.exists(log_file)
        command.log(log_file)
        assert os.path.exists(log_file)

    def test_profile(self):
        cmd = "ls"
        profile = "sge"
        timeout = 1000
        command = Command(cmd, profile, timeout)
        assert command.cmd.startswith("qsub ")
