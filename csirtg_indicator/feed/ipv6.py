import pytricia
from csirtg_indicator.utils.ip import is_ipv6
from csirtg_indicator.constants.networks import V6_RESERVED

PERM_WHITELIST = [
    'FF01:0:0:0:0:0:0:1',
    'FF01:0:0:0:0:0:0:2',
]


def process(data, whitelist=[]):
    wl = pytricia.PyTricia()

    [wl.insert(x, True) for x in PERM_WHITELIST]

    [wl.insert(str(y['indicator']), True) for y in whitelist]

    for i in data:
        if 'whitelist' in set(i['tags']):
            continue

        if not is_ipv6(i['indicator']):
            continue

        if i['indicator'] in V6_RESERVED:
            continue

        if str(i['indicator']) not in wl:
            yield i
