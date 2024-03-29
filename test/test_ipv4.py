from csirtg_indicator import Indicator
from csirtg_indicator.feed.ipv4 import process
import pytest
from faker import Faker
fake = Faker()
import os

DISABLE_FAST_TESTS = os.getenv('DISABLE_NETWORK_TESTS', False)

OUTLIERS = [
    '18.5.4.0/8'
]

FEED = [
    {'indicator': '1.1.1.1', 'tags': ['test']},
    {'indicator': '1.2.3.4', 'tags': ['test']},
    {'indicator': '1.2.3.0/24', 'tags': ['test']},
    {'indicator': '4.3.2.1', 'tags': ['test']},
    {'indicator': '192.168.1.1', 'tags': ['test']},
    {'indicator': '192.168.10.0/24', 'tags': ['test']}
]

FEED_WL = [
    {'indicator': '1.1.1.1', 'tags': ['whitelist']},
    {'indicator': '1.2.0.0/16', 'tags': ['whitelist']}
]


def _not(data):
    for d in data:
        d = Indicator(d)
        assert d.itype is not 'ipv4'


def test_ipv4_ipv6():
    data = ['2001:1608:10:147::21', '2001:4860:4860::8888']
    _not(data)


def test_ipv4_fqdn():
    data = ['example.org', '1.2.3.4.com', 'xn----jtbbmekqknepg3a.xn--p1ai']
    _not(data)


def test_ipv4_urls():
    data = [
        'http://192.168.1.1/1.html',
        'http://www41.xzmnt.com',
        'http://get.ahoybest.com/n/3.6.16/12205897/microsoft lync server 2010.exe'
    ]
    _not(data)


def test_ipv4_ok():
    data = ['192.168.1.0/24', '192.168.1.1', '255.255.255.255']
    for d in data:
        assert Indicator(indicator=d).itype is 'ipv4'


def test_ipv4_nok():
    data = ['127.0.0.0/1', '128.205.0.0/8']
    for d in data:
        Indicator(indicator=d)


def test_ipv4_private():
    data = [
        '128.205.1.0',
        u'106.51.30.0',
        '112.133.246.73'
    ]

    for d in data:
        assert not Indicator(d).is_private

    assert Indicator('172.16.30.32').is_private


def test_ipv4_padded():
    d = {
        '192.168.001.001': '192.168.1.1',
        '192.168.010.1': '192.168.10.1',
        '192.168.100.010': '192.168.100.10',
        '192.168.1.1': '192.168.1.1',
        '012.012.012.012': '12.12.12.12',
        '10.0.0.2': '10.0.0.2',
        '10.0.2.2': '10.0.2.2',
        '10.0.1.0': '10.0.1.0',
        '10.0.0.0/24': '10.0.0.0/24',
        '10.000.00.02': '10.0.0.2'

    }

    for k, v in d.items():
        assert Indicator(k).indicator == v


def test_ipv4_random():
    for d in range(0, 100):
        assert Indicator(indicator=fake.ipv4()).itype == 'ipv4'


def test_ipv4_outliers():
    for i in OUTLIERS:
        assert Indicator(i).itype == 'ipv4'


@pytest.mark.skipif(DISABLE_FAST_TESTS, reason='spamhaus test disabled')
@pytest.mark.xfail
def test_spamhaus():
    i = Indicator('71.6.146.130', resolve_geo=True)
    assert i.spamhaus() is not None


def test_ipv4_feed():

    feed = list(process(FEED, {}))

    assert len(feed) == 4
    assert feed[0]['indicator'] == '1.1.1.1'
    assert feed[1]['indicator'] == '1.2.3.4'
    assert feed[2]['indicator'] == '1.2.3.0/24'
    assert feed[3]['indicator'] == '4.3.2.1'


    feed = list(process(FEED, FEED_WL))

    assert len(feed) == 1
    assert feed[0]['indicator'] == '4.3.2.1'