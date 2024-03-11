"""The configuration module."""
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import tomllib
from attrs import define

if TYPE_CHECKING:
    from typing import NotRequired, Optional, Self

DEFAULT_CONFIG_LOCATION = Path(__file__).parent / Path("default_config.toml")

USER_CONFIG_FILENAME = Path("dicc.toml")

USER_CONFIG_LOCATIONS = [
    Path.home() / Path(".config/dicc/") / USER_CONFIG_FILENAME,  # .config
    Path().home() / Path("." + str(USER_CONFIG_FILENAME)),  # home
]

if xdg_config_home := os.environ.get("XDG_CONFIG_HOME"):
    USER_CONFIG_LOCATIONS.insert(
        0, Path(xdg_config_home) / Path("dicc/") / USER_CONFIG_FILENAME
    )  # xdg_config_home


class CacheSchema(TypedDict):
    """The cache table schema."""

    max_size: int
    max_age: int


class LogSchema(TypedDict):
    """The log table schema."""

    log_level: str  # TODO: Make this Literal


class StyleDisplaySchema(TypedDict):  # TODO: Add to schema as styles are added
    """The style.display table schema."""

    panel: str  # Style applied to the dictionary item border

    item_index: str
    headword: str  # Dictionary item headword, displayed as panel title
    fl: str

    pronunciation_title: str
    pronunciation_content: str

    definition_content: str

    short_def_title: str
    short_def_content: str

    stem_title: str
    stem_content: str

    rules_style: str

    searched_word: str
    pronunciation: str


class StyleTagsSchema(TypedDict):
    """The style.tags table schema."""

    bold: str
    italic: str
    small_caps: str
    subscript: str
    superscript: str
    glossary: str
    paragraph_word: str
    phrase: str
    quote_word: str
    run_in_word: str

    bold_colon: str
    l_double_quote: str
    r_double_quote: str

    cross_reference: str


class StyleSchema(TypedDict):
    """The style table schema."""

    display: StyleDisplaySchema
    tags: StyleTagsSchema


class ConfigSchema(TypedDict):
    """The toml configuration file schema."""

    cache: NotRequired[CacheSchema]
    log: NotRequired[LogSchema]
    style: NotRequired[StyleSchema]


@define
class Configuration:
    """The `dicc` configuration."""

    cache: CacheSchema
    log: LogSchema
    style: StyleSchema

    @staticmethod
    def _load_file(path: Path) -> ConfigSchema:
        with open(path, "rb") as file:
            # I promise this is OK, mypy
            config: ConfigSchema = tomllib.load(file)  # type: ignore [assignment]
            return config

    @staticmethod
    def _find_user_file(locations: list[Path]) -> Optional[Path]:
        for location in locations:
            if location.exists() and location.is_file():
                return location

        return None

    @classmethod
    def load(cls) -> Self:
        """Load the user configuration."""
        default_values = Configuration._load_file(DEFAULT_CONFIG_LOCATION)

        default_config = cls(
            cache=default_values["cache"],  # Can use direct lookup here
            log=default_values["log"],
            style=default_values["style"],
        )

        user_paths = Configuration._find_user_file(USER_CONFIG_LOCATIONS)
        if not user_paths:  # No user configuration found
            return default_config

        # console.print("user config found") # TODO: Logs

        user_config = default_config  # Overly verbose
        user_values = Configuration._load_file(user_paths)

        if user_cache := user_values.get("cache"):
            user_config.cache = user_cache
        if user_log := user_values.get("log"):
            user_config.log = user_log
        if user_style := user_values.get("style"):
            user_config.style = user_style

        return user_config


CONFIG = Configuration.load()
