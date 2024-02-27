"""Interact with the cache through the CLI."""

import sqlite3

import typer

from dicc import cache
from dicc.cache import clear_cache, get_cache
from dicc.terminal import console

app = typer.Typer()


@app.command()
def show() -> None:
    """Display searched words in the cache."""
    db = cache.create_cache_path(cache.CACHE_PATH)
    con = sqlite3.connect(db)

    if not (cached_items := get_cache(con)):
        # Show nothing
        return

    # Print items
    for item in cached_items:
        console.print(item.word)

    con.close()


@app.command()
def clear() -> None:
    """Clear all searched words from the cache."""
    db = cache.create_cache_path(cache.CACHE_PATH)
    con = sqlite3.connect(db)

    clear_cache(con)

    con.close()


if __name__ == "__main__":
    app()
