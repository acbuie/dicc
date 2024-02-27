from dicc import url


def test_dictionary_url() -> None:
    url_ = url._dictionary_url("testing", "api_test")
    assert url_ == (
        "https://www.dictionaryapi.com/api/v3/references/collegiate/"
        "json/testing/?key=api_test"
    )


def test_thesaurus_url() -> None:
    url_ = url._thesaurus_url("testing", "api_test")
    assert url_ == (
        "https://www.dictionaryapi.com/api/v3/references/thesaurus/"
        "json/testing/?key=api_test"
    )
