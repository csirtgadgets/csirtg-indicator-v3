from .fqdn import process as process_fqdn
from .ipv4 import process as process_ipv4
from .ipv6 import process as process_ipv6


def process(data, whitelist, itype=None):
    if itype == 'ipv4':
        yield process_ipv4(data, whitelist)

    elif itype == 'ipv6':
        yield process_ipv6(data, whitelist)

    elif itype == 'fqdn':
        yield process_ipv6(data, whitelist)

    else:
        whitelist = set(whitelist)

        for i in data:
            if 'whitelist' in set(i['tags']):
                continue

            if i['indicator'] in whitelist:
                continue

            yield i


def aggregate(data, field='indicator', sort='confidence',
              sort_secondary='reported_at'):
    x = set()
    rv = []
    for d in sorted(data, key=lambda x: x[sort], reverse=True):
        if d[field] not in x:
            x.add(d[field])
            rv.append(d)

    rv = sorted(rv, key=lambda x: x[sort_secondary], reverse=True)
    return rv
