"""The `Collegiate` API object, and associated functions to display it."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from attrs import define
from rich.console import Group
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from dicc.config import CONFIG
from dicc.display.common import format_text
from dicc.display.format_element import format_dt, format_quotations
from dicc.responses.abstract import MerriamWebsterItem
from dicc.responses.collegiate import (
    AlternateHeadwords,
    Artwork,
    BindingSubstitute,
    CognateCrossReferences,
    CollegiateResponseItem,
    Date,
    DefinedRunOns,
    DefiningText,
    Definitions,
    DirectionalCrossReferences,
    Etymologies,
    FunctionalLabel,
    GeneralLabels,
    HeadwordInformation,
    Homograph,
    Inflections,
    Meta,
    ParenthesizedSenseSequence,
    Quotations,
    Sense,
    SenseArray,
    SenseNumber,
    ShortDef,
    SubjectLabels,
    Synonyms,
    TruncatedSense,
    TruncatedSenseArray,
    UndefinedRunOns,
    Usages,
    Variants,
)
from dicc.responses.collegiate import Table as MWTable

if TYPE_CHECKING:
    from typing import Self

    from rich.console import Console, ConsoleOptions, RenderResult


def _format_sense_values(
    sn: Optional[SenseNumber]
) -> tuple[Optional[int], Optional[str], Optional[str]]:
    major_sense = None
    minor_sense = None
    seq_sense = None

    if not sn:
        return (major_sense, minor_sense, seq_sense)

    sn_vals = sn.split()
    for val in sn_vals:
        try:
            major_sense = int(val)
        except ValueError:
            if len(val) == 3:
                seq_sense = val
            else:
                minor_sense = val

    return (major_sense, minor_sense, seq_sense)


@define
class DefinitionRow:
    """Data to be input into the definition table."""

    major_sense: Optional[int]
    minor_sense: Optional[str]
    seq_sense: Optional[str]
    unformatted_text: Text

    @property
    def maj_sen_text(self) -> Text:
        if not self.major_sense:
            return Text(" ")
        return Text(str(self.major_sense), style="bold bright_white")

    @property
    def min_sen_text(self) -> Text:
        if not self.minor_sense:
            return Text("   ")
        return Text(self.minor_sense, style="bold white")

    @property
    def seq_sen_text(self) -> Text:
        if not self.seq_sense:
            return Text("   ")
        return Text(f"{self.seq_sense} ", style="italic blue")

    @property
    def formatted_text(self) -> Text:
        return format_text(self.unformatted_text)


def _format_sense(sense: Sense) -> DefinitionRow:
    sn = sense.get("sn")
    sen_vals = _format_sense_values(sn)

    dt = sense["dt"]
    defn = format_dt(dt)

    # for item in dt:
    #     if item[0] == "text":
    #         defn = Text(item[1])

    row = DefinitionRow(sen_vals[0], sen_vals[1], sen_vals[2], defn)

    return row


# BUG: Fails on `green`, no `et`
def _format_truncated_sense(sen: TruncatedSense) -> DefinitionRow:
    sn = sen.get("sn")
    sen_vals = _format_sense_values(sn)

    ets = sen["et"]
    for et in ets:
        if et[0] == "text":
            et_text = Text(et[1])

    row = DefinitionRow(sen_vals[0], sen_vals[1], sen_vals[2], et_text)

    return row


def _format_pseq(pseq: ParenthesizedSenseSequence) -> list[DefinitionRow]:
    rows = []
    for pseq_item in pseq[1]:
        if pseq_item[0] == "sense":
            rows.append(_format_sense(pseq_item[1]))
        elif pseq_item[0] == "bs":
            sense_obj = pseq_item[1]
            rows.append(_format_sense(sense_obj["sense"]))

    return rows


def _format_sense_item(
    sense_item: SenseArray
    | TruncatedSenseArray
    | BindingSubstitute
    | ParenthesizedSenseSequence,
    table: Table,
) -> None:
    definition_rows: list[DefinitionRow] = []

    # Mypy seemed to be angry with a match...case setup for this
    if sense_item[0] == "sense":
        definition_rows.append(_format_sense(sense_item[1]))

    elif sense_item[0] == "pseq":
        data = _format_pseq(sense_item)
        for row in data:
            definition_rows.append(row)

    elif sense_item[0] == "bs":
        sense_obj = sense_item[1]
        definition_rows.append(_format_sense(sense_obj["sense"]))

    elif sense_item[0] == "sen":
        definition_rows.append(_format_truncated_sense(sense_item[1]))

    for row in definition_rows:
        table.add_row(
            row.maj_sen_text, row.min_sen_text, row.seq_sen_text, row.formatted_text
        )

    return


@define
class Collegiate(MerriamWebsterItem):
    """Merriam-Webster collegiate dictionary entry."""

    index: int
    meta: Meta
    hwi: HeadwordInformation
    fl: Optional[FunctionalLabel] = None
    defn: Optional[Definitions] = None
    hom: Optional[Homograph] = None
    ahws: Optional[AlternateHeadwords] = None
    vrs: Optional[Variants] = None
    cxs: Optional[CognateCrossReferences] = None
    ins: Optional[Inflections] = None
    lbs: Optional[GeneralLabels] = None
    sls: Optional[SubjectLabels] = None
    uros: Optional[UndefinedRunOns] = None
    dros: Optional[DefinedRunOns] = None
    dxnls: Optional[DirectionalCrossReferences] = None
    et: Optional[Etymologies] = None
    usages: Optional[Usages] = None
    synonyms: Optional[Synonyms] = None
    quotes: Optional[Quotations] = None
    art: Optional[Artwork] = None
    table: Optional[MWTable] = None
    date: Optional[Date] = None
    shortdef: Optional[ShortDef] = None

    @classmethod
    def from_json(cls, json_response: CollegiateResponseItem, index: int) -> Self:
        """Construct a dictionary item from JSON."""
        # Can use direct lookup for items always present
        meta = json_response["meta"]
        hwi = json_response["hwi"]

        # Use `.get()` method otherwise
        fl = json_response.get("fl")
        defn = json_response.get("def")
        hom = json_response.get("hom")
        ahws = json_response.get("ahws")
        vrs = json_response.get("vrs")
        cxs = json_response.get("cxs")
        ins = json_response.get("ins")
        lbs = json_response.get("lbs")
        sls = json_response.get("sls")
        uros = json_response.get("uros")
        dros = json_response.get("dros")
        dxnls = json_response.get("dxnls")
        et = json_response.get("et")
        usages = json_response.get("usages")
        synonyms = json_response.get("synonyms")
        quotes = json_response.get("quotes")
        art = json_response.get("art")
        table = json_response.get("table")
        date = json_response.get("date")
        shortdef = json_response.get("shortdef")

        # Leaving like this in case I want to do some sort of validation later

        return cls(
            index=index,
            meta=meta,
            hwi=hwi,
            fl=fl,
            defn=defn,
            hom=hom,
            ahws=ahws,
            vrs=vrs,
            cxs=cxs,
            ins=ins,
            lbs=lbs,
            sls=sls,
            uros=uros,
            dros=dros,
            dxnls=dxnls,
            et=et,
            usages=usages,
            synonyms=synonyms,
            quotes=quotes,
            art=art,
            table=table,
            date=date,
            shortdef=shortdef,
        )

    def format_panel_title(self) -> Text:
        """Format the dictionary item title."""
        dict_index_text = Text(
            f" {self.index + 1} ", style=CONFIG.style["display"]["item_index"]
        )
        panel_title_spacing = Text(" ── ", style=CONFIG.style["display"]["panel"])
        headword_text = Text(
            self.meta["id"].replace(":", " : "),
            style=CONFIG.style["display"]["headword"],
        )

        # BUG: Waiting on https://github.com/Textualize/rich/issues/2745 to merge
        # At the moment, the panel style will overwrite the title style.

        # NOTE: This wasn't working, but now it is. Keep an eye on this perhaps?

        panel_title = (
            Text("")
            .append_text(dict_index_text)
            .append_text(panel_title_spacing)
            .append_text(headword_text)
        )

        if functional_label := self.fl:
            fl_text = Text(functional_label, style=CONFIG.style["display"]["fl"])
            panel_title.append_text(panel_title_spacing).append_text(fl_text)

        return panel_title

    def format_pronunciations(self) -> Optional[Text]:
        """Format the dictionary item pronunciations."""
        if not (pronunciations := self.hwi.get("prs")):
            return None

        pronunciation_separator = Text(" | ")  # Separate pronunciations
        pronunciation_text = pronunciation_separator.join(
            [
                Text(pron["mw"], style=CONFIG.style["display"]["pronunciation_content"])
                for pron in pronunciations
            ]
        )

        pronunciation_line = (
            Text("")
            # .append_text(
            #     Text("Pronunciation:", style=CONFIG.style["pronunciation_title"])
            # )
            # .append_text(Text(" "))
            .append_text(pronunciation_text)
        )

        return pronunciation_line

    def format_short_defs(self) -> Optional[Text]:
        """Format the dictionary item short definitions."""
        if not (shortdefs := self.shortdef):
            return None

        shortdef_separator = Text("\n")
        shortdef_text = shortdef_separator.join(
            [
                Text(f"• {defs}", style=CONFIG.style["display"]["short_def_content"])
                for defs in shortdefs
            ]
        )

        shortdef_line = (
            Text("")
            .append_text(
                Text(
                    "Short Definition:",
                    style=CONFIG.style["display"]["short_def_title"],
                )
            )
            .append_text(Text("\n"))
            .append_text(shortdef_text)
        )

        return shortdef_line

    def format_stems(self) -> Optional[Text]:
        """Format the dictionary item headword stems."""
        if not (stems := self.meta.get("stems")):
            return None

        stem_separator = Text(" | ")
        stem_text = stem_separator.join(
            [
                Text(stem, style=CONFIG.style["display"]["stem_content"])
                for stem in stems
            ]
        )

        stem_line = (
            Text("")
            .append_text(Text("Stems:", style=CONFIG.style["display"]["stem_title"]))
            .append_text(Text(" "))
            .append_text(stem_text)
        )

        return stem_line

    def format_date(self) -> Optional[Text]:
        """Format the dictionary item date text."""
        if not (date := self.date):
            return None

        unformatted_text = Text(date)
        formatted_date = format_text(unformatted_text)

        date_line = (
            Text()
            .append_text(Text("First Known Use:\n", style="white underline"))
            .append_text(formatted_date)
        )

        return date_line

    def format_defns(self) -> Optional[Group]:
        """Format the dictionary item defintions and sense sequences."""
        if not (defns := self.defn):
            return None

        definition_tables = []

        for defn in defns:
            layout = Table.grid()
            layout.add_column(
                width=1,
                justify="left",
            )  # Integer `sn`, major numbers
            layout.add_column(
                width=3,
                justify="center",
            )  # Character `sn`, subsense a, b, ...
            layout.add_column(
                width=4,
                justify="left",
            )  # Character `sn`, pseq (1), (2), ...
            layout.add_column()  # Definition column

            # Get top level objects
            if verb_div := defn.get("vd"):
                verb_text = Text(verb_div, style="bold italic cyan")

            else:
                verb_text = None

            # if subject_lbl := defn.get("sls"):
            #     text_placeholder.append(subject_lbl)

            if sense_seq := defn.get("sseq"):
                for sense_group in sense_seq:
                    for sense_item in sense_group:
                        _format_sense_item(sense_item, layout)

            all_renderables = [verb_text, layout]
            renderables = [renderable for renderable in all_renderables if renderable]

            definition_tables.append(Group(*renderables))

        return Group(*definition_tables, "")

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Render the dictionary item to the terminal."""
        # Panel title
        panel_title = self.format_panel_title()

        # Pronunciations
        pronunciations = self.format_pronunciations()

        defns = self.format_defns()

        # Short definitions
        short_defs = None
        if not defns:
            short_defs = self.format_short_defs()

        # console.print(self.defn)

        stems = self.format_stems()

        date = self.format_date()

        quotes = format_quotations(self.quotes)

        # console.print(self.quotes)

        all_renderables = [pronunciations, defns, short_defs, stems, date, quotes]
        renderables = [renderable for renderable in all_renderables if renderable]

        renderable_group = Group(*renderables)

        yield Rule(panel_title, align="left", style=CONFIG.style["display"]["panel"])
        yield renderable_group
        yield str()  # Empty line between items
