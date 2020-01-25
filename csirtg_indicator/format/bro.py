import re
from csirtg_indicator import Indicator

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


itype = {
    'ipv4': 'ADDR',
    'ipv6': 'ADDR',
    'url': 'URL',
    'fqdn': 'DOMAIN',
    'md5': 'FILE_HASH',
    'sha1': 'FILE_HASH',
    'sha256': 'FILE_HASH',
}

COLUMNS = ['fields', 'indicator', 'indicator_type', 'meta.desc',
           'meta.confidence', 'meta.source', 'meta.do_notice']

COLUMNS_DEFAULT = ['indicator', 'itype', 'tags', 'confidence', 'provider']

HEADER = '#' + '\t'.join(COLUMNS)
SEP = '|'


def _i_to_bro(i, cols=COLUMNS_DEFAULT):
    r = []
    
    if i['itype'] is 'url':
        i['indicator'] = re.sub(r'(https?\:\/\/)', '', i['indicator'])

    for c in cols:
        y = i.get(c, '-')

        if type(y) is list:
            y = SEP.join(y)

        if isinstance(y, int):
            y = str(y)

        if c is 'itype':
            y = 'Intel::{0}'.format(itype[i[c]])

        r.append(str(y))

    # do_notice
    # https://www.bro.org/bro-exchange-2013/exercises/intel.html
    # https://github.com/csirtgadgets/massive-octo-spice/issues/438
    r.append('T')
    return "\t".join(r)


def get_lines(data, cols=COLUMNS_DEFAULT):
    output = StringIO()
    output.write("{0}\n".format(HEADER))

    if not isinstance(data, list):
        data = [data]

    for i in data:
        if isinstance(i, Indicator):
            i = i.__dict__()

        i = _i_to_bro(i, cols)

        output.write(i)
        output.write("\n")

        yield output.getvalue()

        if isinstance(output, StringIO):
            output.truncate(0)
