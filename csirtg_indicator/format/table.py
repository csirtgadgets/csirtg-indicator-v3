from prettytable import PrettyTable
import arrow
from csirtg_indicator import Indicator
from csirtg_indicator.constants import COLUMNS, MAX_FIELD_SIZE
from csirtg_indicator.utils import list_to_csv
from pprint import pprint


def _indicator_row(i, cols, max_field_size):
    if isinstance(i, Indicator):
        i = i.__dict__()

    r = []
    for c in cols:

        y = i.get(c, '')

        if isinstance(y, list) and y[0] is not None:
            y = list_to_csv(y)

        if c == 'confidence' and y is None:
            y = 0.0

        if y and (c in ['first_at', 'last_at', 'reported_at']):
            y = arrow.get(y).format('YYYY-MM-DDTHH:mm:ss.SSSSS')
            y = '{}Z'.format(y)
        else:
            y = str(y)
        y = (y[:max_field_size] + '..') if len(y) > max_field_size else y

        r.append(y)

    return r


def get_lines(data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
    t = PrettyTable(cols)

    if not isinstance(data, list):
        data = [data]

    for i in data:
        t.add_row(_indicator_row(i, cols, max_field_size))

    yield str(t)
