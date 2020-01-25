from csirtg_indicator import Indicator
import json
from random import randint, uniform
from pprint import pprint
import arrow


def test_indicator_ipv4():
    i = Indicator('192.168.1.1')
    assert i.is_private
    assert i.indicator == '192.168.1.1'
    assert i.itype == 'ipv4'


def test_indicator_fqdn():
    i = Indicator('example.org')

    assert i.is_private is False
    assert i.indicator == 'example.org'
    assert i.itype == 'fqdn'


def test_indicator_url():
    i = Indicator('http://example.org', tags='botnet,malware')

    assert i.is_private is False
    assert i.indicator == 'http://example.org'
    assert i.itype is not 'fqdn'
    assert i.itype is 'url'
    assert 'botnet' in i.tags
    assert 'malware' in i.tags


def test_indicator_str():
    i = Indicator('http://example.org', tags='botnet,malware')

    s = json.loads(str(i))

    assert 'botnet' in s['tags']

    i = Indicator(**s)

    assert 'malware' in i.tags


def test_get_set():
    i = Indicator('localhost.com')

    try:
        i.indicator = 'localhost'
    except TypeError:
        pass

    i.indicator = 'localhost.org'
    assert i.itype == 'fqdn'

    i.indicator = 'https://192.168.1.1'
    assert i.itype == 'url'

    assert str(i)
    print(i)


def test_indicator_dest():
    i = Indicator(indicator='192.168.1.1', dest='10.0.0.1', portlist="23",
                  protocol="tcp", dest_portlist='21,22-23')
    assert i.dest
    assert i.dest_portlist


def test_confidence_str():
    c = uniform(0.001, 9.99)
    assert Indicator(indicator='192.168.1.1', confidence=c).confidence == c

    try:
        Indicator(indicator='192.168.1.1', confidence=',')
        raise RuntimeError('should not set confidence to ,')
    except ValueError:
        pass


def test_count_str():
    c = randint(0, 500)
    assert Indicator(indicator='192.168.1.1', count=c).count == c

    try:
        Indicator(indicator='192.168.1.1', count=',')
        raise RuntimeError('should not set confidence to ,')
    except ValueError:
        pass


def test_uuid():
    u1 = Indicator(indicator='192.168.1.1').uuid
    u2 = Indicator(indicator='192.168.1.1').uuid

    assert u1 is not None
    assert u2 is not None
    assert u1 != u2


def test_eq():
    reported_at = arrow.utcnow()
    u1 = Indicator(indicator='192.168.1.1', reported_at=reported_at)
    u2 = Indicator(indicator='192.168.1.1', reported_at=reported_at)

    u2.uuid = u1.uuid
    assert u1 == u2


def test_copy():
    i1 = Indicator('128.205.1.1', tags='malware')
    i2 = i1.copy(tags='pdns', reported_at=arrow.utcnow())

    assert i1 != i2
    assert i1.tags != i2.tags
    assert i1.uuid != i2.uuid


def test_is_itype():
    assert Indicator('128.205.1.1', tags='malware').is_ipv4
    assert Indicator('128.205.1.1', tags='malware').is_ip
    assert Indicator('example.com', tags='malware').is_fqdn
    assert Indicator('http://example.com', tags='malware').is_url


def test_get_attr():
    i = Indicator('128.205.1.1', tags='malware')
    assert i.get('tags')
