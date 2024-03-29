"""Common functions for parsing and displaying data."""

import re

from rich.style import Style
from rich.text import Text

from dicc.config.main import CONFIG

# TODO: Standardize these functions so they behave in the same way


def _remove_tag(text: Text, tag: str) -> Text:
    """Remove all occurences of one tag."""
    final_text = Text()

    split = text.split(separator=tag)
    [final_text.append_text(line) for line in split]

    return final_text


def _remove_tag_pair(text: Text, open_tag: str, close_tag: str) -> Text:
    """Remove all occurences of two tags, as an open and closing tag."""
    # NOTE: There is probably a clever way to do this with recursion.

    initial_text = Text()
    final_text = Text()

    initial_text.append_text(_remove_tag(text, open_tag))
    final_text.append_text(_remove_tag(initial_text, close_tag))

    return final_text


def _stylize_at_tag(
    text: Text,
    pattern: str,
    replacement: Text,
) -> Text:
    """Replace a single tag, as regex pattern, with `Text`."""
    simple_text = text.plain

    search = re.compile(pattern)
    first_hit = search.search(simple_text)

    if not first_hit:
        return text

    coord = first_hit.span()
    start_index = coord[0]
    end_index = coord[1]

    text = text[:start_index] + replacement + text[end_index:]

    return text


def _stylize_at_tag_recursive(text: Text, pattern: str, replacement: Text) -> Text:
    """Recursively replace a single tag, as regex pattern, with `Text`."""
    simple_text = text.plain

    search = re.compile(pattern)
    first_hit = search.search(simple_text)

    if not first_hit:
        return text

    coord = first_hit.span()
    start_index = coord[0]
    end_index = coord[1]

    text = text[:start_index] + replacement + text[end_index:]

    text = _stylize_at_tag_recursive(text, pattern, replacement)

    return text


def _format_tag_ds(text: Text) -> Text:
    """Format the date sense token ({ds||||}).

    Only occurs in `Date`.
    """
    starting_text = Text(", in the meaning of ")

    pattern = "{ds(.*?)}"
    searcher = re.compile(pattern)

    first_hit = searcher.search(text.plain)

    if not first_hit:
        return text

    _, vd, sn_num, sn_letter, sn_paren = first_hit.group().split(
        "|"
    )  # Mypy might complain

    match vd:
        case "t":
            vd_text = Text("transitive", style="italic")
        case "i":
            vd_text = Text("intransitive", style="italic")
        case _:
            vd_text = Text("")

    if sn_num:
        sn_num_text = Text(f"sense {sn_num}", style="italic")
    else:
        sn_num_text = Text("")

    if sn_letter:
        sn_letter_text = Text(sn_letter, style="italic")
    else:
        sn_letter_text = Text("")

    if sn_paren:
        sn_paren_text = Text(sn_paren[:-1], style="italic")
    else:
        sn_paren_text = Text("")

    replacement_text = (
        starting_text + vd_text + sn_num_text + sn_letter_text + sn_paren_text
    )

    final_text = _stylize_at_tag_recursive(text, pattern, replacement_text)

    return final_text


def _format_cross_reference(text: Text, tag: str, style: str) -> Text:
    """Format cross reference tags."""
    pattern = f"{{{tag}(.*?)}}"
    searcher = re.compile(pattern)

    first_hit = searcher.search(text.plain)

    if not first_hit:
        return text

    # TODO: For now, just grab the second field
    split = first_hit.group(1).split("|")
    display_text = split[1]

    replacement_text = Text(display_text, style=style)

    final_text = _stylize_at_tag(text, pattern, replacement_text)

    # Recursive to grab all instances of the tag
    recursive_text = _format_cross_reference(final_text, tag, style)

    return recursive_text


def _format_run_in(text: Text) -> Text:
    """Remove any erroneous newlines, often from run ins."""
    open_pattern = r"(\(\n)"  # Generally no space after the open paren
    close_pattern = r"(\n\s\))"

    text = _stylize_at_tag(text, open_pattern, Text("("))
    text = _stylize_at_tag(text, close_pattern, Text(" )"))
    return text


def format_text(text: Text) -> Text:
    """Remove tags and format the replacement text accordingly."""
    tag_pairs = [
        "b",
        "it",
        "sc",
        "inf",
        "sup",
        "gloss",
        "parahw",
        "phrase",
        "qword",
        "wi",
    ]

    tag_solo = [
        "bc",
        "ldquo",
        "rdquo",
    ]

    tag_special = [
        "ds",  # Date sense token
        "ri",  # Format weird run in text
    ]

    tag_cross_reference_pairs = [
        "dx",
        "dx_def",
        "dx_ety",
        "ma",
    ]

    tag_cross_reference = [
        "a_link",
        "d_link",
        "i_link",
        "et_link",
        "mat",
        "sx",
        "dxt",
    ]

    styles = [
        CONFIG.style["tags"]["bold"],
        CONFIG.style["tags"]["italic"],
        CONFIG.style["tags"]["small_caps"],
        CONFIG.style["tags"]["subscript"],
        CONFIG.style["tags"]["superscript"],
        CONFIG.style["tags"]["glossary"],
        CONFIG.style["tags"]["paragraph_word"],
        CONFIG.style["tags"]["phrase"],
        CONFIG.style["tags"]["quote_word"],
        CONFIG.style["tags"]["run_in_word"],
        CONFIG.style["tags"]["bold_colon"],
        CONFIG.style["tags"]["l_double_quote"],
        CONFIG.style["tags"]["r_double_quote"],
        None,
        None,
        None,
        None,
        None,
        None,
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
        CONFIG.style["tags"]["cross_reference"],
    ]

    replacements = [  # When a token is entirely substituted
        ": ",
        '"',
        '"',
    ]

    all_replacements: list[None | str] = [
        *[None] * len(tag_pairs),
        *replacements,
        *[None] * len(tag_special),
        *[None] * len(tag_cross_reference_pairs),
        *[None] * len(tag_cross_reference),
    ]

    all_tags = [
        *tag_pairs,
        *tag_solo,
        *tag_special,
        *tag_cross_reference_pairs,
        *tag_cross_reference,
    ]

    for tag, style, replacement in zip(all_tags, styles, all_replacements):
        match tag:
            case (
                "b"
                | "it"
                | "sc"
                | "inf"
                | "sup"
                | "parahw"
                | "phrase"
                | "qword"
                | "wi"
            ):
                open_pattern = f"{{{tag}}}"
                close_pattern = rf"{{/{tag}}}"
                between_pattern = f"(?<={{{tag}}})(.*?)(?={{\\/{tag}}})"

                text.highlight_regex(between_pattern, Style.parse(style))

                text = _remove_tag_pair(text, open_pattern, close_pattern)

            case "gloss":
                open_pattern = "{gloss}"
                close_pattern = r"{/gloss}"

                open_replacement = Text("[", style=style)
                close_replacement = Text("]", style=style)

                open_text = _stylize_at_tag(text, open_pattern, open_replacement)
                text = _stylize_at_tag(open_text, close_pattern, close_replacement)

            # TODO: Refactor into function with "gloss"
            case "dx_def":
                open_pattern = "{dx_def}"
                close_pattern = r"{/dx_def}"

                open_replacement = Text("(", style=style)
                close_replacement = Text(")", style=style)

                open_text = _stylize_at_tag(text, open_pattern, open_replacement)
                text = _stylize_at_tag(open_text, close_pattern, close_replacement)

            case "bc" | "ldquo" | "rdquo":
                pattern = f"{{{tag}}}*"

                if not replacement:
                    raise ValueError("Missing required text.")

                replacement_text = Text(replacement, Style.parse(style))

                text = _stylize_at_tag(text, pattern, replacement_text)

            case "ds":
                text = _format_tag_ds(text)

            case "ri":
                text = _format_run_in(text)

            case "dx" | "dt_ety":
                open_pattern = f"{{{tag}}}"
                close_pattern = rf"{{/{tag}}}"

                replacement_text = Text("\n — ")

                text = _stylize_at_tag(text, open_pattern, replacement_text)
                text = _remove_tag_pair(text, open_pattern, close_pattern)

            case "a_link" | "d_link" | "i_link" | "et_link" | "mat" | "sx" | "dxt":
                text = _format_cross_reference(text, tag, style)

            case _:
                # Not handled
                pass
    return text
