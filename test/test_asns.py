from csirtg_indicator import Indicator


def _not(data):
    for d in data:
        try:
            d = Indicator(d)
            assert d.itype is not 'asn'
        except TypeError:
            pass


def test_asn_nok():
    data = [
        'example.com',
        'http://example.com:81',
        '192.168.1.1',
        '127.0.0./1'
    ]

    _not(data)


def test_asn_random():
    for d in [1, 10, 500, 65535]:
        assert Indicator(indicator='AS{}'.format(d)).itype == 'asn'
        print(Indicator(indicator='AS{}'.format(d)))
