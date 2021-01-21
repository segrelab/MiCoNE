"""
    Custom spinner class
"""

from typing import Optional

from halo import Halo
from click import echo


class Spinner:
    """
    A custom spinner class that makes use of `halo` and `click`

    Parameters
    ----------
    text : str
    spinner : str

    Attributes
    ----------
    interactive : bool
        True if the `Spinner` instance is interactive
    text : str
        The text currently in the spinner
    """

    def __init__(self, text: str, spinner: str, interactive: bool = True) -> None:
        self.interactive = interactive
        self._text = text
        if self.interactive:
            self._spinner = Halo(text=self._text, spinner=spinner)
        else:
            self._spinner = None

    @property
    def text(self) -> str:
        """ The text in the spinner """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        if self.interactive:
            self._spinner.text = self._text
        else:
            echo(self._text)

    def start(self) -> None:
        """ Start the spinner """
        if self.interactive:
            self._spinner.start()

    def succeed(self, text: Optional[str] = None) -> None:
        """ Display text on success """
        if text:
            self._text = text
        if self.interactive:
            self._spinner.succeed(self.text)
        else:
            echo(self.text)

    def fail(self, text: Optional[str] = None) -> None:
        """ Display text on failure """
        if text:
            self._text = text
        if self.interactive:
            self._spinner.fail(self.text)
        else:
            echo(self.text)

    def stop(self) -> None:
        """ Stop the spinner """
        if self.interactive:
            self._spinner.stop()
        self._text = ""
