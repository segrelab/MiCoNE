"""
    Tests for `mindpipe` package
"""

import pytest

from click.testing import CliRunner

from mindpipe import mindpipe
from mindpipe import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "Main entry point to mindpipe" in result.output
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output
