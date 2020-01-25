
import pytricia
from csirtg_indicator.utils.ip import is_ipv4
from csirtg_indicator.constants.networks import V4_RESERVED

LARGEST_PREFIX = '8'


def _normalize(i):
    bits = i.split('.')

    rv = []
    for b in bits:
        if len(b) > 1 and b.startswith('0') and not b.startswith('0/'):
            b = b[1:]
        rv.append(b)

    i = '.'.join(rv)

    return i


# https://github.com/jsommers/pytricia
def process(data=[], whitelist=[]):
    wl = pytricia.PyTricia()

    for y in whitelist:
        y = str(_normalize(y['indicator']))
        # weird bug work-around it'll insert 172.16.1.60 with a /0 at the end??
        if '/' not in y:
            y = '{}/32'.format(y)

        wl[y] = True

    for i in data:
        if 'whitelist' in set(i['tags']):
            continue

        i['indicator'] = _normalize(i['indicator'])

        if not is_ipv4(i['indicator']):
            continue

        if i['indicator'] in V4_RESERVED:
            continue

        if str(i['indicator']) not in wl:
            yield i
