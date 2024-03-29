"""Common functions for the `query` subpackage."""
from __future__ import annotations

import datetime
import json
import sqlite3
from typing import TYPE_CHECKING, NamedTuple

import httpx
from rich.text import Text

from dicc import cache, url
from dicc.display.collegiate import Collegiate
from dicc.display.no_response import InvalidSearch
from dicc.terminal import console

if TYPE_CHECKING:
    from dicc.responses.abstract import MerriamWebsterItem
    from dicc.responses.collegiate import CollegiateResponse


class MerriamWebsterQuery(NamedTuple):
    """Query to send to Merriam Webster."""

    word: str
    timestamp: datetime.datetime
    method: url.QueryMethod
    query_url: httpx.URL


def create_query(word: str, method: url.QueryMethod) -> MerriamWebsterQuery:
    """Create the seach query."""
    url_ = url.build_url(word, method)
    query_ = MerriamWebsterQuery(word, datetime.datetime.now(), method, url_)

    return query_


def process_query(
    query: MerriamWebsterQuery,
    con: sqlite3.Connection,
    client: httpx.Client,
) -> list[MerriamWebsterItem]:
    """Send a query to Merriam-Webster's API."""
    # Check if cached
    if cache_record := cache.get_row(con, query.query_url):
        json_response = json.loads(cache_record.response_text)
    else:
        response = client.get(query.query_url).raise_for_status()
        json_response = response.json()

    # Insert into cache if pulled from API
    if not cache_record:
        cache.insert_row(con, query, json.dumps(json_response))

    data: list[MerriamWebsterItem] = []

    # No result, or list of alternate search terms
    if not json_response or isinstance(json_response[0], str):
        json_response: list[str]  # type: ignore [no-redef]

        message = (
            "No results found for the searched term. Perhaps you meant one of "
            "the following?"
        )

        console.print(Text(message, style="italic red"))

        for index, item in enumerate(json_response):
            data.append(InvalidSearch.from_json(item, index))

        return data

    match query.method:
        case "dictionary":
            json_response: CollegiateResponse  # type: ignore [no-redef]

            for index, item in enumerate(json_response):
                data.append(Collegiate.from_json(item, index))

        # case "thesaurus":
        #     json_response: ThesaurusResponse
        #     thesaurus = Thesaurus.from_json(json_response)
        #     data = thesaurus

        case _:
            raise ValueError("Invalid query method.")

    return data
