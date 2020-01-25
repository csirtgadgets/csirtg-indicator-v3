from csirtg_indicator import Indicator


def test_confidence():
    i = Indicator('128.205.1.1', tags='scanner')
    assert i.confidence == 4

    i = Indicator('128.205.1.1')
    assert i.confidence == 0

    i = Indicator('http://go0gle.com/1.html', tags='phishing')
    assert i.confidence == 4
