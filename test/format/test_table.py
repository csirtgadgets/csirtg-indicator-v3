# -*- coding: utf-8 -*-
import pytest
from csirtg_indicator.format.table import get_lines
from csirtg_indicator import Indicator


@pytest.fixture
def indicator():
    i = {
            'indicator': "example.com",
            'itype': 'fqdn',
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reported_at': '2015-01-01T00:00:00Z',
            'asn_desc': u'telefÔnica brasil'
        }
    return Indicator(**i)


@pytest.fixture
def indicator_unicode(indicator):
    indicator.indicator = 'http://xz.job391.com/down/ï¿½ï¿½ï¿½ï¿½à¿ªï¿½ï¿½@89_1_60'
    return indicator


def test_format_table(indicator):

    s = list(get_lines([indicator]))
    assert len(s) > 0

    n = indicator.to_table()
    assert "example.com" in n


def test_format_table_unicode(indicator_unicode):

    s = list(get_lines([indicator_unicode]))
    assert len(s) > 0


if __name__ == '__main__':
    test_format_table()
