"""
    Module containing tests for the template_renderers
"""

import pytest

from mindpipe.pipelines import ConfigTemplate, ScriptTemplate


@pytest.mark.usefixtures("config_template_files")
class TestTemplate:
    """ Tests for the ConfigTemplate and ScriptTemplate class """

    def test_config_template(self, config_template_files):
        template_file = config_template_files[0]["input"]
        with open(config_template_files[0]["output"], 'r') as fid:
            config_str = fid.read()
        config_template = ConfigTemplate(template_file)
        data = config_template_files[1]
        with open("temp.txt", 'w') as fid:
            fid.write(config_template.render(data))
        config_str_created = config_template.render(data)
        assert config_str.strip() == config_str_created.strip()

    def test_script_template(self):
        pass
