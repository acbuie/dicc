"""The `InvalidSearch` object."""
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from attrs import define

from dicc.responses.abstract import MerriamWebsterItem

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


@define
class InvalidSearch(MerriamWebsterItem):
    """Invalid search term."""

    index: int
    alternate_term: str

    @classmethod
    def from_json(cls, json: str, index: int) -> Self:
        """Construct an invalid response from JSON."""
        return cls(alternate_term=json, index=index)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Render the invalid search item to the terminal."""
        yield (self.alternate_term)
