
from csirtg_indicator import Indicator
from csirtg_indicator.constants import COLUMNS


def get_lines(data, cols=COLUMNS):
    if not isinstance(data, list):
        data = [data]

    for i in data:
        if isinstance(i, Indicator):
            i = i.__dict__()

        r = dict()
        for c in cols:
            y = i.get(c, u'')

            if type(y) is list:
                y = u'|'.join(y)

            if c == 'confidence' and y is None:
                y = 0.0

            r[c] = y
            if isinstance(r[c], (str, bytes)):
                r[c] = r[c].replace('\n', r'\\n')

        yield ','.join([str(r[v]) for v in r])
