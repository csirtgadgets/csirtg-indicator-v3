import json
from csirtg_indicator import Indicator
from csirtg_indicator.constants import COLUMNS
from csirtg_indicator.utils import list_to_csv


def _indicator_row(i, cols):
    if isinstance(i, Indicator):
        i = i.__dict__()

    r = dict()
    for c in cols:
        y = i.get(c, u'')
        if isinstance(y, list):
            y = list_to_csv(y)

        r[c] = y

    return r


def get_lines(data, cols=COLUMNS, stream=False):
    for i in data:

        i = _indicator_row(i, cols)

        if stream:
            i = [i]

        yield json.dumps(i)
