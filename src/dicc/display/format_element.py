"""Common functions for formating specific API elements."""
from typing import Optional

from rich.text import Text

from dicc.config import CONFIG
from dicc.display.common import format_text
from dicc.responses.collegiate import (
    AttributionQuote,
    BiographicalNameElement,
    CalledAlsoElement,
    DefiningText,
    Quotations,
    RunInElement,
    SupplementalNoteElement,
    UsageNoteElement,
    VerbalIllustrationElement,
)
from dicc.terminal import console


def format_aq(aq: AttributionQuote) -> Text:
    """Construct and format `Text` from an attribution quote.

    Attribution of quote occurs in verbal illustrations and quotes.
    """
    text = Text(" ↳ ")

    aq_list = []

    if auth := aq.get("auth"):
        aq_list.append(Text(auth))

    if source := aq.get("source"):
        aq_list.append(Text(source))

    if aq_date := aq.get("aqdate"):
        aq_list.append(Text(aq_date))

    if subsource := aq.get("subsource"):
        sub_text = Text()
        if subsource_source := subsource.get("source"):
            sub_text.append_text(Text(subsource_source))

        if subsource_aqdate := subsource.get("aqdate"):
            sub_text.append_text(Text(f", {subsource_aqdate}"))

        aq_list.append(sub_text)

    joined = Text(", ").join(aq_list)
    text.append_text(joined)

    return text


def format_vis(vis: list[VerbalIllustrationElement]) -> Text:
    """Format the verbal illustration section."""
    vis_separator = Text("\n")
    vis_texts = []

    for vis_item in vis:
        em_dash = Text(" — ")
        vis_text = em_dash.append_text(Text(vis_item["t"]))

        if aq := vis_item.get("aq"):
            aq_text = format_aq(aq)
            vis_text.append_text(Text("\n")).append_text(aq_text)

        vis_texts.append(vis_text)

    vis_line = vis_separator.join(vis_texts)

    return vis_line


def format_ri(ri: list[RunInElement]) -> Text:
    """Format the run in section."""
    ri_text = Text(" ")

    for element in ri:
        # If a list, we have RunInWrap or RunInBuffer
        if isinstance(element, list):
            if element[0] == "riw":
                rie = element[1]["rie"]
                ri_text.append_text(Text(rie))

            elif element[0] == "text":
                intervening_text = Text(element[1])
                ri_text.append_text(intervening_text)

        # If not, we have Pronunciation or Variant
        else:
            # TODO: Handle `Pronunciation` and `Variants`
            print(element)

    return ri_text


def format_snote(snote: list[SupplementalNoteElement]) -> Text:
    """Format the supplemental note section."""
    text_line = Text("NOTE: ")
    # text_line.stylize("grey42", end=-1)  # NOTE: This works with `on` styles

    for element in snote:
        if element[0] == "t":
            text_line.append_text(Text(element[1]))

        elif element[0] == "vis":
            vis_line = Text("\n") + format_vis(element[1])
            text_line.append_text(vis_line)

        elif element[0] == "ri":
            ri_line = format_ri(element[1])
            text_line.append_text(ri_line)

    return text_line


def format_uns(uns: list[UsageNoteElement]) -> Text:
    """Format the usage note section."""
    items_separator = Text("\n")
    items = []

    for usage_note in uns:
        for element in usage_note:
            if element[0] == "text":
                # Always present
                items.append(Text(f"-> {element[1]}", style="white"))

            elif element[0] == "vis":
                vis_line = format_vis(element[1])
                vis_line.stylize("grey42")
                items.append(vis_line)

            elif element[0] == "ri":
                ri_line = format_ri(element[1])
                items.append(ri_line)

    final_line = items_separator.join(items)

    return final_line


def format_ca(ca: CalledAlsoElement) -> Text:
    """Format the called also section."""
    items_separator = Text(", ")
    items = []

    intro_text = Text(f"-> {ca["intro"]} ")

    ca_targets = ca["cats"]
    for ca_target in ca_targets:
        items.append(Text(f"{{it}}{ca_target["cat"]}{{/it}}"))

        if prs := ca_target.get("prs"):
            console.print(prs)
            pass

        if psl := ca_target.get("psl"):
            console.print(psl)
            pass

        if pn := ca_target.get("pn"):
            console.print(pn)
            pass

    final_text = intro_text + items_separator.join(items)

    return final_text


# def format_bnw(bnw: BiographicalNameElement) -> Text:
#     """Format the biographical name wrap section."""
#     pass


def format_dt(dt: DefiningText) -> Text:
    """Format the defining text section."""
    # Set all to empty `Text`, which acts like `None` but we can use `+`
    item_separator = Text("\n")
    items = []

    for item in dt:
        if item[0] == "text":
            dt_element_line = Text(
                item[1], style=CONFIG.style["display"]["definition_content"]
            )
            items.append(dt_element_line)

        elif item[0] == "uns":
            uns_line = format_uns(item[1])
            items.append(uns_line)

        elif item[0] == "vis":
            vis_line = format_vis(item[1])
            vis_line.stylize("grey42")
            items.append(vis_line)

        elif item[0] == "ca":
            ca_line = format_ca(item[1])
            # console.print(f"{ca=}")
            items.append(ca_line)

        elif item[0] == "bnw":
            bnw = item[1]
            console.print(f"{bnw=}")

        elif item[0] == "ri":
            ri_line = format_ri(item[1])
            ri_line.stylize(CONFIG.style["display"]["definition_content"])
            items.append(ri_line)

        elif item[0] == "snote":
            snote_line = format_snote(item[1])
            snote_line.stylize("grey42")  # stylize after for consistent styling
            items.append(snote_line)

    final_text = item_separator.join(items)

    return final_text


def format_quotations(quotes: Optional[Quotations]) -> Optional[Text]:
    """Format the quotations section."""
    if not quotes:
        return None

    quote_separator = Text("\n")

    quote_lines = []
    quote_lines.append(Text("Examples:"))

    for quote in quotes:
        quote_text = Text(quote["t"])
        aq_text = format_aq(quote["aq"])

        quote_line = quote_text + Text("\n") + aq_text
        quote_lines.append(quote_line)

    unformatted_text = quote_separator.join(quote_lines)
    final_text = format_text(unformatted_text)

    return final_text
