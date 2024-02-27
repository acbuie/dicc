"""Main entrypoint to the CLI."""

from typing import Annotated, Optional

import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from dicc.cli import cache
from dicc.query.main import search_word
from dicc.terminal import console

app = typer.Typer(pretty_exceptions_show_locals=False)


def autocomplete_search_method(incomplete: str) -> list[str]:
    """List of valid flags for the --method CLI option in `search`."""
    valid_names = ("collegiate", "c", "thesaurus", "t")
    completion = []
    for name in valid_names:
        if name.startswith(incomplete):
            completion.append(name)

    return completion


@app.callback()
def set_width(width: Optional[int] = None) -> None:
    """Set the width of the console."""
    if not width:
        return

    console.width = width


@app.command()
def search(
    word: str,
    method: Annotated[
        str,
        typer.Option(
            "--method",
            "-m",
            help="Search with alternative API method",
            autocompletion=autocomplete_search_method,
        ),
    ] = "collegiate",
) -> None:
    """Search for WORD in the Collegiate API.

    If --method, search for WORD in the given API.
    """
    match method:
        case "collegiate" | "c":
            result = search_word(word, "dictionary")

        case "thesaurus" | "t":
            result = search_word(word, "thesaurus")

    dict_item_renderables = Group(*result)
    console.print(
        Panel(
            dict_item_renderables,
            title=Text(word.upper(), style="bold white"),
            title_align="center",
        ),
    )


app.add_typer(cache.app, name="cache")


def run() -> None:
    """Run the CLI."""
    app()
