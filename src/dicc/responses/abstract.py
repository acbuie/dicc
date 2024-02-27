"""The `MerriamWebsterItem` protocol."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, Self

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


class MerriamWebsterItem(Protocol):
    """Merriam-Webster item protocol."""

    @classmethod
    def from_json(cls, json: Any, index: int) -> Self:  # `Any` is JSON
        """Create an instance from JSON data."""
        ...

    def __rich_console__(
        self, console: Console, console_options: ConsoleOptions
    ) -> RenderResult:
        ...
