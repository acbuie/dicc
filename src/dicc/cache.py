"""The caching module."""
from __future__ import annotations

import datetime
import pathlib
import sqlite3
from typing import TYPE_CHECKING, Literal, NamedTuple

if TYPE_CHECKING:
    from typing import Optional

import httpx

from dicc.query.common import MerriamWebsterQuery

CACHE_PATH = pathlib.Path().home() / ".cache" / "dicc"


class CacheRecord(NamedTuple):
    """Query data payload, also equivalent to a row in the cache DB."""

    word: str  # Our searched word
    created_timestamp: datetime.datetime
    search_method: Literal["dictionary", "thesaurus"]
    query_url: httpx.URL
    response_text: str  # TODO: This is our JSON response


def adapt_datetime_utc(value: datetime.datetime) -> str:
    """Convert `datetime` object to SQL timestamp."""
    return value.isoformat()


def adapt_url(value: httpx.URL) -> str:
    """Convert `URL` object to SQL text."""
    return str(value)


sqlite3.register_adapter(datetime.datetime, adapt_datetime_utc)
sqlite3.register_adapter(httpx.URL, adapt_url)


def create_cache_path(cache_path: pathlib.Path) -> pathlib.Path:
    """Create the `dicc` cache."""
    cache_path.mkdir(parents=True, exist_ok=True)

    db = cache_path / "dicc.db"
    return db


def create_database(con: sqlite3.Connection) -> None:
    """Create the cache database tables."""
    # Word query table
    with con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS queries (
            "word" TEXT NOT NULL,
            "created_timestamp" TEXT NOT NULL,
            "search_method" TEXT NOT NULL,
            "query_url" TEXT NOT NULL PRIMARY KEY,
            "response_text" TEXT NOT NULL
            )
            """
        )


def get_cache(con: sqlite3.Connection) -> Optional[list[CacheRecord]]:
    """Get the entire cache table, if it contains any records."""
    with con:
        cur = con.execute("SELECT * FROM queries")

        data = cur.fetchall()

    if not data:
        return None

    cache = [CacheRecord._make(row) for row in data]

    return cache


def clear_cache(con: sqlite3.Connection) -> None:
    """Delete all rows from the cache table, effectively clearing the cache."""
    with con:
        con.execute("DELETE FROM queries")


def insert_row(
    con: sqlite3.Connection,
    query: MerriamWebsterQuery,
    response: str,
) -> CacheRecord:
    """Insert a query into the cache."""
    word, timestamp, method, query_url = query

    with con:
        con.execute(
            """INSERT INTO queries  
        (word, created_timestamp, search_method, query_url, response_text) 
        VALUES (?, ?, ?, ?, ?)""",
            (
                word,
                timestamp,
                method,
                query_url,
                response,
            ),
        )

    row = CacheRecord(word, timestamp, method, query_url, response)

    return row


def delete_row(con: sqlite3.Connection, url: httpx.URL) -> Optional[CacheRecord]:
    """Delete a query from the cache."""
    with con:
        cur = con.execute(
            "SELECT * FROM queries WHERE query_url = ?",
            (url,),
        )

        data = cur.fetchall()

        if not data:
            return None

        con.execute(
            "DELETE FROM queries WHERE query_url = ?",
            (url,),
        )

    row = CacheRecord._make(data)

    return row


def get_row(con: sqlite3.Connection, url: httpx.URL) -> Optional[CacheRecord]:
    """Return a row from the cache, if it exists."""
    with con:
        cur = con.execute(
            "SELECT * FROM queries WHERE query_url = ?",
            (url,),
        )

        data = cur.fetchone()

        if not data:
            return None

    row = CacheRecord._make(data)

    return row
