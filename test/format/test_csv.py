# -*- coding: utf-8 -*-
from csirtg_indicator import Indicator
import pytest
from csirtg_indicator.format.csv import get_lines


@pytest.fixture
def indicator():
    i = {
            'indicator': "example.com",
            'itype': 'fqdn',
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reported_at': '2015-01-01T00:00:00Z'
        }
    return Indicator(**i)


@pytest.fixture
def indicator_unicode(indicator):
    indicator.indicator = 'http://xz.job391.com/down/ï¿½ï¿½ï¿½ï¿½à¿ªï¿½ï¿½@89_1_60'
    return indicator


def test_format_csv(indicator):

    n = list(get_lines([indicator, indicator]))
    assert len(n) > 0

    n = indicator.to_csv()
    assert "example.com" in n
