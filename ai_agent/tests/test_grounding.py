from ai_agent.service import numbers


def test_equivalent_number_formatting_is_allowed():
    assert numbers('1 817 300,00 и 0.3000') == numbers('1817300.0 и 0.3')
    assert numbers('1.2e-05') == numbers('0.000012')
    assert not numbers('1 800 000') <= numbers('1817300.0')


def test_identifiers_do_not_pass_through_float():
    assert numbers('#900000000000000001') != numbers('#900000000000000002')
