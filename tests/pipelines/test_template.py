"""
    Module containing tests for the template_renderers
"""

import pytest

from micone.pipelines import ConfigTemplate, ScriptTemplate


@pytest.mark.usefixtures("config_template_files", "script_template_files")
class TestTemplate:
    """ Tests for the ConfigTemplate and ScriptTemplate class """

    def test_config_template(self, config_template_files):
        template_file = config_template_files[0]["input"]
        with open(config_template_files[0]["output"], "r") as fid:
            config_str = fid.read()
        config_template = ConfigTemplate(template_file)
        data = config_template_files[1]
        config_str_created = config_template.render(data)
        assert config_str.strip() == config_str_created.strip()

    def test_script_template(self, script_template_files):
        template_file, process_folder = script_template_files
        with open(template_file["output"], "r") as fid:
            script_str = fid.read()
        script_template = ScriptTemplate(template_file["input"], process_folder)
        data = {}
        script_str_created = script_template.render(data)
        assert script_str.strip() == script_str_created.strip()
