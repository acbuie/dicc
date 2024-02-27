from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, Literal

import httpx

from dicc import cache
from dicc.query.common import create_query, process_query

if TYPE_CHECKING:
    from dicc.responses.abstract import MerriamWebsterItem


def search_word(
    word: str, method: Literal["dictionary", "thesaurus"]
) -> list[MerriamWebsterItem]:
    """Search for a word."""
    db = cache.create_cache_path(cache.CACHE_PATH)
    con = sqlite3.connect(db)
    client = httpx.Client()

    query_ = create_query(word, method)

    try:
        result = process_query(query_, con, client)
    except sqlite3.OperationalError:
        cache.create_database(con)
        result = process_query(query_, con, client)

    con.close()

    return result
