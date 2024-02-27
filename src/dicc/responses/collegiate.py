"""Merriam-Webster's Collegiate dictionary API response, modelled as `TypedDict`."""

from typing import Literal, NotRequired, Optional, TypedDict


# Section 2.1, meta
class Meta(TypedDict):
    """The metadata entry.

    Section 2.1
    """

    id: str
    uuid: str
    sort: str
    src: str
    section: str
    stems: list[str]
    offsensive: bool


# Section 2.6 (out of order), prs
class Sound(TypedDict):
    """The sound entry.

    No Section.
    """

    audio: str
    ref: str
    stat: int


class Pronunciation(TypedDict):  # NOTE: Wrapped in an array
    """The pronunciation entry.

    Section 2.6
    """

    mw: NotRequired[str]
    l: NotRequired[str]  # noqa
    l2: NotRequired[str]
    pun: NotRequired[str]
    sound: NotRequired[Sound]


Pronunciations = list[Pronunciation]  # Plural

# Section 2.7.4 (out of order), psl
ParenthesizedSubjectLabel = str


# Section 2.7.5 (out of order), spl
class SenseSpecificInflectionPluralLabel(TypedDict):
    """The sense-specific inflection plural label entry.

    Section 2.7.5
    """

    spl: str


# Section 2.2, Homograph, is simply an int, hom
Homograph = int


# Section 2.3, hwi
class HeadwordInformation(TypedDict):
    """The headword information entry.

    The headword is the word that is being defined.

    Section 2.3
    """

    hw: str
    prs: NotRequired[Pronunciations]


# Section 2.4, ahws
class AlternateHeadword(TypedDict):  # NOTE: Wrapped in an array.
    """The alternative headword entry.

    Alternative headwords are other regional or less common spellings of headwords.

    Section 2.4
    """

    hw: str
    prs: NotRequired[Pronunciations]
    psl: NotRequired[ParenthesizedSubjectLabel]


AlternateHeadwords = list[AlternateHeadword]


# Section 2.5, vrs
class Variant(TypedDict):  # NOTE: Wrapped in an array.
    """The variant headword entry.

    Variants are different spellings of headwords.

    Section 2.5
    """

    va: str
    vl: NotRequired[str]
    prs: NotRequired[Pronunciations]
    spl: NotRequired[SenseSpecificInflectionPluralLabel]


Variants = list[Variant]


# Section 2.6 is Pronunciation and Sound, above.

# Section 2.7

# Section 2.7.1, fl
FunctionalLabel = str


# Section 2.7.2, lbs
GeneralLabels = list[str]  # NOTE: Is an array.


# Section 2.7.3, sls
SubjectLabels = list[str]  # NOTE: Is an array.


# Section 2.7.4 is ParenthesizedSubjectLabel, above.


# Section 2.7.5 is SenseSpecificInflectionPluralLabel, above.


# Section 2.7.6, sgram
SenseSpecificGrammaticalLabel = str


# Section 2.8, ins
Inflection = TypedDict(  # NOTE: Wrapped in an array.
    "Inflection",
    {
        "if": NotRequired[str],  # inflection
        "ifc": NotRequired[str],  # inflection cutback
        "il": NotRequired[str],  # inflection label
        "prs": NotRequired[Pronunciations],
        "spl": NotRequired[SenseSpecificInflectionPluralLabel],
    },
)

Inflections = list[Inflection]


# Section 2.9
class CognateCrossReferenceTarget(TypedDict):  # NOTE: Wrapped in an array.
    """The cognate cross-reference targets entry.

    See CognateCrossReference, Section 2.9.
    """

    cxl: NotRequired[str]  # cognate cross-reference label
    cxr: NotRequired[str]  # cross-reference id
    cxt: NotRequired[str]  # hyperlink text, or id when no `cxr`
    cxn: NotRequired[str]  # sense number of target


class CognateCrossReference(TypedDict):  # NOTE: Wrapped in an array.
    """The cognate cross-reference entry.

    When a headword is a less common spelling of another word with the same meaning,
    there will be a cognate cross-reference to the more common headword spelling.

    Section 2.9.
    """

    cxl: str  # cognate cross-reference label
    cxtis: list[CognateCrossReferenceTarget]


CognateCrossReferences = list[CognateCrossReference]


# Section 2.10

# Section 2.10.1, Definition, is below


# Section 2.10.2, vd
VerbDivider = str  # Perhaps a Literal?


# Section 2.10.3, SenseSequence, is below


# Section 2.10.4, Sense, is below


# Section 2.10.5, sn
SenseNumber = str


# Section 2.10.6, DefiningText, is below


# Section 2.10.7, sdsense, is below


# Section 2.10.8, sen, is below


# Section 2.10.9, bs, is below


# Section 2.10.10, pseq, is below


# Section 2.11, VerbalIllustration, is below


# Section 2.12
class Subsource(TypedDict):
    """Container object for subsource information."""

    source: NotRequired[str]
    aqdate: NotRequired[str]


class AttributionQuote(TypedDict):
    """Attribution quote entry.

    Section 2.12
    """

    auth: NotRequired[str]  # author
    source: NotRequired[str]
    aqdate: NotRequired[str]  # publication date
    subsource: NotRequired[Subsource]


# Section 2.11 (out of order), vis
class VerbalIllustrationElement(TypedDict):
    """Verbal illustration text entry.

    Section 2.11
    """

    t: str  # illustration text
    aq: NotRequired[AttributionQuote]


VerbalIllustration = tuple[Literal["vis"], list[VerbalIllustrationElement]]

# Section 2.13, ri
RunInWrap = tuple[Literal["riw"], dict[Literal["rie"], str]]
RunInBuffer = tuple[Literal["text"], str]
RunInElement = RunInWrap | RunInBuffer | Pronunciation | Variant
RunIn = tuple[Literal["ri"], list[RunInElement]]


# Section 2.14, bnw
class BiographicalNameElement(TypedDict):
    """Container object for BiographicalNameWrap."""

    pname: NotRequired[str]
    sname: NotRequired[str]
    altname: NotRequired[str]
    prs: NotRequired[Pronunciations]


BiographicalNameWrap = tuple[Literal["bnw"], BiographicalNameElement]


# Section 2.15, ca
class CalledAlsoTarget(TypedDict):
    """Container object for CalledAlso."""

    cat: str  # called also target
    catref: NotRequired[str]  # called also reference id
    pn: NotRequired[str]  # parenthesized number
    prs: NotRequired[Pronunciation]
    psl: NotRequired[ParenthesizedSubjectLabel]


class CalledAlsoElement(TypedDict):
    """Container object for CalledAlsoNote."""

    intro: Literal["called also"]
    cats: list[CalledAlsoTarget]


CalledAlsoNote = tuple[Literal["ca"], CalledAlsoElement]

# Section 2.16, snote
SupplementalNoteText = tuple[Literal["t"], str]
SupplementalNoteElement = SupplementalNoteText | RunIn | VerbalIllustration
SupplementalNote = tuple[
    Literal["snote"], list[SupplementalNoteElement]
]  # Optional RunIn and VerbalIllustration


# Section 2.17, uns
UsageNoteElement = list[tuple[Literal["text"], str] | RunIn | VerbalIllustration]
UsageNote = tuple[Literal["uns"], list[UsageNoteElement]]


# Section 2.26 (out of order), etymology
EtymologyNote = tuple[Literal["et_snote"], list[tuple[Literal["t"], str]]]
EtymologyContent = tuple[Literal["text"], str]
Etymology = EtymologyContent | EtymologyNote  # NOTE: Wrapped in an array
Etymologies = list[Etymology]

# Section 2.10.6 (out of order), dt
DefiningTextElement = tuple[Literal["text"], str]
DefiningText = list[
    DefiningTextElement
    | BiographicalNameWrap
    | CalledAlsoNote
    | RunIn
    | SupplementalNote
    | UsageNote
    | VerbalIllustration
]


# Section 2.10.7 (out of order), sdense
class DividedSense(TypedDict):
    """The divided sense entry.

    Section 2.10.7
    """

    sd: str
    dt: DefiningText
    et: NotRequired[Etymologies]
    ins: NotRequired[Inflections]
    lbs: NotRequired[GeneralLabels]
    prs: NotRequired[Pronunciations]
    sgram: NotRequired[SenseSpecificGrammaticalLabel]
    sls: NotRequired[SubjectLabels]
    vrs: NotRequired[Variants]


# Section 2.10.8 (out of order), sen
class TruncatedSense(TypedDict):
    """The truncated sense entry.

    Section 2.10.8
    """

    sn: SenseNumber
    et: NotRequired[Etymologies]
    ins: NotRequired[Inflections]
    lbs: NotRequired[GeneralLabels]
    prs: NotRequired[Pronunciations]
    sgram: NotRequired[SenseSpecificGrammaticalLabel]
    sls: NotRequired[SubjectLabels]
    vrs: NotRequired[Variants]


TruncatedSenseArray = tuple[Literal["sen"], TruncatedSense]


# Section 2.10.4 (out of order), sense
class Sense(TypedDict):  # NOTE: Wrapped in an array.
    """The sense entry.

    The sense is a gathering of all material relevant to a headword.

    Section 2.10.4
    """

    sn: NotRequired[SenseNumber]
    dt: DefiningText
    et: NotRequired[Etymologies]
    ins: NotRequired[Inflections]
    lbs: NotRequired[GeneralLabels]
    prs: NotRequired[Pronunciations]
    sdsense: NotRequired[DividedSense]
    sgram: NotRequired[SenseSpecificGrammaticalLabel]
    sls: NotRequired[SubjectLabels]
    vrs: NotRequired[Variants]


SenseArray = tuple[Literal["sense"], Sense]


class SenseObject(TypedDict):
    """Container for sense dictionaries."""

    sense: Sense


# Section 2.10.9 (out of order), bs
BindingSubstitute = tuple[Literal["bs"], SenseObject]


# Section 2.10.10 (out of order), pseq
ParenthesizedSenseSequence = tuple[
    Literal["pseq"], list[BindingSubstitute | SenseArray]
]


# Section 2.10.5 (out of order), sseq
SenseSequence = list[
    list[
        SenseArray
        | TruncatedSenseArray
        | BindingSubstitute
        | ParenthesizedSenseSequence
    ]
]


# Section 2.10.1 (out of order), def
class Definition(TypedDict):  # NOTE: Wrapped in an array.
    """The definition entry.

    Definitions encompass all like content relevant to a meaning of a headword.

    Section 2.10.1.
    """

    sls: NotRequired[SubjectLabels]
    vd: NotRequired[VerbDivider]
    sseq: SenseSequence


Definitions = list[Definition]


# Section 2.18, uros
class UndefinedRunOn(TypedDict):  # NOTE: Wrapped in an array.
    """The undefined run on phrase entry.

    Section 2.18
    """

    ure: str  # undefined entry word
    fl: FunctionalLabel
    utxt: NotRequired[list[VerbalIllustration | UsageNote]]  # usage text
    ins: NotRequired[Inflections]
    lbs: NotRequired[GeneralLabels]
    prs: NotRequired[Pronunciations]
    psl: NotRequired[ParenthesizedSubjectLabel]
    sls: NotRequired[SubjectLabels]
    vrs: NotRequired[Variants]


UndefinedRunOns = list[UndefinedRunOn]


# Section 2.19, dros
class DefinedRunOn(TypedDict):  # NOTE: Wrapped in an array.
    """The defined run on phrase entry.

    Section 2.19
    """

    drp: str  # defined run on phrase
    def_: Definitions  # NOTE: Key is actually `def`
    et: NotRequired[Etymologies]
    lbs: NotRequired[GeneralLabels]
    prs: NotRequired[Pronunciations]
    psl: NotRequired[ParenthesizedSubjectLabel]
    sls: NotRequired[SubjectLabels]
    vrs: NotRequired[Variants]


DefinedRunOns = list[DefinedRunOn]


# Section 2.20, dxnls
DirectionalCrossReferences = list[str]


# Section 2.21, usages
class UsageRef(TypedDict):
    uaref: str


ParagraphText = list[tuple[Literal["text"], str] | VerbalIllustration | UsageRef]


class Usage(TypedDict):  # NOTE: Wrapped in an array.
    pl: str  # paragraph label
    pt: ParagraphText


Usages = list[Usage]


# Section 2.22
class SeeAdditional(TypedDict):
    sarefs: list[str]


SynonymText = list[tuple[Literal["text"], str] | VerbalIllustration | SeeAdditional]


class Synonym(TypedDict):  # NOTE: Wrapped in an array.
    pl: str
    pt: SynonymText


Synonyms = list[Synonym]


# Section 2.23
class Quotation(TypedDict):  # NOTE: Wrapped in an array.
    t: str  # quotation text
    aq: AttributionQuote


Quotations = list[Quotation]


# Section 2.24
class Artwork(TypedDict):
    artid: str
    capt: str


# Section 2.25
class Table(TypedDict):
    tableid: str
    displayname: str


# Section 2.27
Date = str


# Section 2.28
ShortDef = list[str]


CollegiateResponseItem = TypedDict(
    "CollegiateResponseItem",
    {
        "meta": Meta,
        "hom": NotRequired[Homograph],
        "hwi": HeadwordInformation,
        "ahws": NotRequired[AlternateHeadwords],
        "vrs": NotRequired[Variants],
        "fl": NotRequired[FunctionalLabel],
        "cxs": NotRequired[CognateCrossReferences],
        "ins": NotRequired[Inflections],
        "lbs": NotRequired[GeneralLabels],
        "sls": NotRequired[SubjectLabels],
        "def": NotRequired[Definitions],  # Functional syntax needed for keyword
        "uros": NotRequired[UndefinedRunOns],
        "dros": NotRequired[DefinedRunOns],
        "dxnls": NotRequired[DirectionalCrossReferences],
        "et": NotRequired[Etymologies],
        "usages": NotRequired[Usages],
        "synonyms": NotRequired[Synonyms],
        "quotes": NotRequired[Quotations],
        "art": NotRequired[Artwork],
        "table": NotRequired[Table],
        "date": NotRequired[Date],
        "shortdef": NotRequired[ShortDef],  # Maybe always present?
    },
)


CollegiateResponse = list[CollegiateResponseItem]
