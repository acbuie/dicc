"""Construct the `httpx.URL` for a seach query."""
from collections.abc import Callable
from typing import Literal

import httpx

QueryProtocol = Callable[[str, str], httpx.URL]
QueryMethod = Literal["dictionary", "thesaurus"]


def _dictionary_url(word: str, api_key: str) -> httpx.URL:
    """Construct the `URL` for a dictionary query."""
    base_url = httpx.URL(
        "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    )  # NOTE: Maybe move this?

    url = base_url.join(f"{word}/?key={api_key}")

    return url


def _thesaurus_url(word: str, api_key: str) -> httpx.URL:
    """Construct the `URL` for a thesaurus query."""
    base_url = httpx.URL(
        "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
    )

    url = base_url.join(f"{word}/?key={api_key}")

    return url


def _url_query_factory(method: QueryMethod) -> tuple[QueryProtocol, str]:
    """Provide the proper query function and api key for a query method."""
    if method == "dictionary":
        return _dictionary_url, "dictionary_api"
    elif method == "thesaurus":
        return _thesaurus_url, "thesaurus_api"
    else:
        raise ValueError("Invalid query method.")


def build_url(word: str, method: QueryMethod) -> httpx.URL:
    """Provide the `URL` for a search query."""
    url_query_callable, api_key = _url_query_factory(method)
    url = url_query_callable(word, api_key)
    return url


if __name__ == "__main__":
    url = build_url("blue", "thesaurus")

    print(url)
