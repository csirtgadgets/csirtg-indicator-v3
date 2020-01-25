# -*- coding: utf-8 -*-
from csirtg_indicator.format.snort import get_lines
from csirtg_indicator import Indicator
import pytest


import re
RULE_PATTERN = r'^alert (TCP|UDP|IP) (\S+) (\S+) -> ([^,]+)\s(\S+)\s\([^.]+\)'

@pytest.fixture
def indicator():
    i = {
        'indicator': "example.com",
        'provider': "me.com",
        'tlp': "amber",
        'confidence': "85",
        'reported_at': '2015-01-01T00:00:00Z',
        'itype': 'fqdn',
        'tags': 'botnet'
    }
    return Indicator(**i)


def test_format_snort(indicator):
    data = [
        indicator, indicator
    ]

    text = "\n".join(list(get_lines(data)))
    assert text
    assert re.findall(RULE_PATTERN, text)

    n = indicator.to_snort()
    assert "example.com" in n


def test_format_snort_extra_params(indicator):
    data = [
        indicator, indicator
    ]

    text = "\n".join(list(get_lines(data)))
    assert text
    assert re.findall(RULE_PATTERN, text)

    n = indicator.to_snort()
    assert "example.com" in n


if __name__ == '__main__':
    test_format_snort()
