"""
    Module that renders the Jinja templates
"""

import pathlib
from typing import Dict, Set

from jinja2 import Environment, FileSystemLoader, meta


class Template:
    """
        Base class for manipulating and rendering Jinja2 templates

        Parameters
        ----------
        template_file : pathlib.Path
            The path to the Jinja2 template file

        Attributes
        ----------
        template_vars : Set[str]
            The set of undeclared variables in the template
    """

    def __init__(self, template_file: pathlib.Path) -> None:
        loader = FileSystemLoader(str(template_file.parent))
        self._env = Environment(loader=loader)
        self._template = self._env.get_template(template_file.name)
        source, *_ = self._env.loader.get_source(self._env, template_file.name)
        self._vars = meta.find_undeclared_variables(self._env.parse(source))

    def render(self, template_data: dict) -> str:
        """
            Render the template using the data passed in as arguments

            Parameters
            ----------
            template_data : dict
                Dictionary of data used to fill in the template

            Returns
            -------
            str
                The rendered template

            Raises
            ------
            UndefinedError
                If an undeclared variable is not provided a value in template_data
        """
        return self._template.render(template_data)

    @property
    def template_vars(self) -> Set[str]:
        """
            The variables in the template
        """
        return self._vars


class ScriptTemplate(Template):
    """
        The class for templating nextflow pipeline scripts

        Parameters
        ----------
        script_file : pathlib.Path
            The path to the nextflow script template
        process_dir : pathlib.Path
            The path to the directory containing process scripts for the script_file

        Attributes
        ----------
        template_vars : Set[str]
            The set of undeclared variables in the template
        process_scripts : Dict[str, str]
            The process scripts of the nextflow pipeline
    """

    def __init__(self, script_file: pathlib.Path, process_dir: pathlib.Path) -> None:
        super().__init__(script_file)
        self._process_dir = process_dir

    @property
    def process_scripts(self) -> Dict[str, str]:
        """
            The process scripts of the nextflow pipeline
        """
        wrapper = '"""\n'
        indent = ' ' * 4
        scripts: Dict[str, str] = {}
        for file in self._process_dir.iterdir():
            if file.stem in self.template_vars:
                with open(file, 'r') as fid:
                    line_list = fid.readlines()
                    data = ''.join(map(lambda x: indent + x, line_list))
                    scripts[file.stem] = wrapper + data + indent + wrapper
        return scripts

    def render(self, template_data: dict) -> str:
        """
            Render the nextflow script template

            Parameters
            ----------
            template_data : dict
                Dictionary of data used to fill in the template
                This data in addition to the process scripts that are handled automatically

            Returns
            -------
            str
                The rendered template
        """
        data = {**self.process_scripts, **template_data}
        return super().render(data)


class ConfigTemplate(Template):
    """
        Class for templating nextflow configuration files

        Parameters
        ----------
        config_file : pathlib.Path
            The path to the configuration file

        Attributes
        ----------
        template_vars : Set[str]
            The set of undeclared variables in the template
    """

    def __init__(self, config_file: pathlib.Path) -> None:
        super().__init__(config_file)
