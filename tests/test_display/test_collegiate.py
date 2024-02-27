from dicc.display.collegiate import _format_sense_values


def test_format_sense_values() -> None:
    """Test the parsing and handling of possible sense number values."""
    sn_1 = "1"
    sn_2 = "1 a"
    sn_3 = "1 a (1)"
    sn_4 = "a"
    sn_5 = "a (1)"
    sn_6 = "(1)"
    sn_7 = "1 (1)"
    sn_8 = None

    values_1 = (1, None, None)
    values_2 = (1, "a", None)
    values_3 = (1, "a", "(1)")
    values_4 = (None, "a", None)
    values_5 = (None, "a", "(1)")
    values_6 = (None, None, "(1)")
    values_7 = (1, None, "(1)")
    values_8 = (None, None, None)

    assert values_1 == _format_sense_values(sn_1)
    assert values_2 == _format_sense_values(sn_2)
    assert values_3 == _format_sense_values(sn_3)
    assert values_4 == _format_sense_values(sn_4)
    assert values_5 == _format_sense_values(sn_5)
    assert values_6 == _format_sense_values(sn_6)
    assert values_7 == _format_sense_values(sn_7)
    assert values_8 == _format_sense_values(sn_8)
