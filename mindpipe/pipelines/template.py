"""
    Module that renders the Jinja templates
"""

import pathlib
from typing import Dict

from jinja2 import Environment, FileSystemLoader
from jinja2schema import infer


CONFIG_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent / "config/configs"


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
        self._vars = infer(source)

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
    def template_vars(self) -> dict:
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
        indent = " " * 4
        scripts: Dict[str, str] = {}
        for file in self._process_dir.iterdir():
            if file.stem in self.template_vars:
                with open(file, "r") as fid:
                    line_list = fid.readlines()
                    data = "".join(map(lambda x: indent + x, line_list))
                    scripts[file.stem] = wrapper + data + indent + wrapper
        return scripts

    def render(self, template_data: dict = dict()) -> str:
        """
            Render the nextflow script template

            Parameters
            ----------
            template_data : dict, optional
                Dictionary of data used to fill in the template
                This data in addition to the process scripts that are handled automatically
                Default is an empty dictionary

            Returns
            -------
            str
                The rendered template
        """
        data = {**self.process_scripts, **template_data}
        return super().render(data)


class ResourceTemplate(Template):
    """ Class for templating nextflow resource files """

    pass


class ProfileTemplate(Template):
    """ Class for templating nextflow profile files """

    pass


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

    _resource_config: pathlib.Path = CONFIG_DIR / "resources.config"
    _profile_config: pathlib.Path = CONFIG_DIR / "profiles.config"

    def __init__(self, config_file: pathlib.Path) -> None:
        super().__init__(config_file)

    def render(self, template_data: dict, resource_config: bool = False) -> str:
        """
            Render the template using the data passed in as arguments

            Parameters
            ----------
            template_data : dict
                Dictionary of data used to fill in the template
            resource_config : bool, optional
                Flag to determine whether to append profile and resouce configs
                Default value is False

            Returns
            -------
            str
                The rendered template

            Raises
            ------
            UndefinedError
                If an undeclared variable is not provided a value in template_data
        """
        rendered_config = self._template.render(template_data)
        if resource_config:
            resource_template = ResourceTemplate(self._resource_config)
            resource = resource_template.render(template_data)
            profile_template = ProfileTemplate(self._profile_config)
            profile = profile_template.render(template_data)
        else:
            resource = ""
            profile = ""
        return rendered_config + resource + profile
