from dicc.display.common import (
    _remove_tag,
    _remove_tag_pair,
    _stylize_at_tag,
)
from rich.text import Text


def test_remove_tag() -> None:
    input_text_1 = Text(r"an example {ldquo}")
    input_text_2 = Text(r"{bc}an {rdquo}example")
    input_text_3 = Text(r"{bc}an {bc}example{bc}")

    removed_text_1 = Text("an example ")
    removed_text_2 = Text("an {rdquo}example")
    removed_text_3 = Text("an example")

    assert removed_text_1 == _remove_tag(input_text_1, "{ldquo}")
    assert removed_text_2 == _remove_tag(input_text_2, "{bc}")
    assert removed_text_3 == _remove_tag(input_text_3, "{bc}")


def test_remove_tag_pair() -> None:
    input_text_1 = Text(r"an example {b}bold me{/b}")
    input_text_2 = Text(r"an example {it}italic me{/it}")
    input_text_3 = Text(r"an example {b}bold me{/b} and also {b}me{/b}")
    input_text_4 = Text(r"an example {sup}sup me{/sup} and also {sup}me{/sup}")

    removed_text_1 = Text("an example bold me")
    removed_text_2 = Text("an example italic me")
    removed_text_3 = Text("an example bold me and also me")
    removed_text_4 = Text("an example sup me and also me")

    assert removed_text_1 == _remove_tag_pair(input_text_1, "{b}", r"{/b}")
    assert removed_text_2 == _remove_tag_pair(input_text_2, "{it}", r"{/it}")
    assert removed_text_3 == _remove_tag_pair(input_text_3, "{b}", r"{/b}")
    assert removed_text_4 == _remove_tag_pair(input_text_4, "{sup}", r"{/sup}")


def test_stylize_at_tag() -> None:
    input_text_1 = Text(r"an example {ldquo}")
    input_text_2 = Text(r"{bc}an {rdquo}example")
    input_text_3 = Text(r"{bc}an {bc}example{bc}")

    removed_text_1 = Text('an example "')
    removed_text_2 = Text(":an {rdquo}example")
    removed_text_3 = Text(":an :example:")

    assert removed_text_1 == _stylize_at_tag(input_text_1, "{ldquo}", Text('"'))
    assert removed_text_2 == _stylize_at_tag(input_text_2, "{bc}", Text(":"))
    assert removed_text_3 == _stylize_at_tag(input_text_3, "{bc}", Text(":"))
