"""
    Module that renders the Jinja templates
"""

import pathlib

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
        template_vars : set
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
    def template_vars(self) -> set:
        """
            The variables in the template
        """
        return self._vars

# render_template
# init ScriptTemplate(JinjaTemplate)
# init ConfigTemplate(JinjaTemplate)
