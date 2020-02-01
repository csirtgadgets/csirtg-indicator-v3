import json
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from base64 import b64encode
import logging
import uuid
import copy
import arrow

from csirtg_indicator.constants import V4_RESERVED, VERSION, \
    FIELDS, FIELDS_TIME, LOG_FORMAT, VERSION, GEO, PEERS, FQDN, BASESTRING


from .wrappers.formatter import FormatterMixin
from .wrappers.itypes import ItypesMixin
from .wrappers.properties import PropertiesMixin
from .wrappers.spamhaus import Spamhaus as SpamhausMixin
from .wrappers.farsight import Farsight as FarsightMixin
from .wrappers.csirtg import Csirtg as CsirtgMixin
from .wrappers.cif import Cif as CifMixin
from .wrappers.geo import Geo as GeoMixin
from .wrappers.peers import Peers as PeersMixin
from .wrappers.dns import DNS as DNSMixin


class Indicator(PropertiesMixin, FormatterMixin,
                ItypesMixin, SpamhausMixin, FarsightMixin, CsirtgMixin,
                DNSMixin, CifMixin, GeoMixin, PeersMixin):

    def __init__(self, indicator=None, **kwargs):
        self.version = VERSION

        self._init_fields(**kwargs)

        if indicator:
            self.indicator = indicator

        # geo, fqdn, peers
        self._init_metadata(**kwargs)

    def _init_metadata(self, **kwargs):
        self.resolve_geo = kwargs.get('resolve_geo', GEO)
        self.resolve_peers = kwargs.get('resolve_peers', PEERS)
        self.resolve_fqdn = kwargs.get('resolve_fqdn', FQDN)

        if self.resolve_fqdn:
            self.fqdn_resolve()

        if self.resolve_geo:
            self.geo_resolve()

        if self.resolve_peers:
            self.peers_resolve()

    def _init_fields(self, **kwargs):
        for k in FIELDS:
            # handle these at the end
            if k in ['indicator', 'confidence', 'count']:
                setattr(self, f"_{k}", None)
                continue

            if kwargs.get(k) is None:
                v = None

                setattr(self, k, v)
                continue

            # set this at the end
            if k in FIELDS_TIME:
                continue

            if isinstance(kwargs[k], BASESTRING):
                kwargs[k] = kwargs[k].lower()
                if k in ['tags', 'peers', 'ptags', 'upstream', 'downstream']:
                    kwargs[k] = kwargs[k].split(',')

            setattr(self, k, kwargs[k])

        for k in FIELDS_TIME:
            setattr(self, k, kwargs.get(k, None))

        self.confidence = kwargs.get('confidence', None)
        self.count = kwargs.get('count', 1)
        self.uuid = kwargs.get('uuid', str(uuid.uuid4()))
        self.group = kwargs.get('group', 'everyone')
        self.tlp = kwargs.get('tlp', 'AMBER')
        self.asn_desc = None

        # incoming id
        self.iid = kwargs.get('iid')

        # outgoing id (if any)
        self.oid = kwargs.get('oid')

        if not self.reported_at:
            self.reported_at = arrow.utcnow().datetime

    def copy(self, **kwargs):
        try:
            i = Indicator(**copy.deepcopy(self.__dict__()))

            for k in kwargs:
                setattr(i, k, kwargs[k])

            i.uuid = str(uuid.uuid4())
            if not i.tags:
                i.tags = []

            if not isinstance(i.tags, list):
                i.tags = [i.tags]

            if not kwargs.get('last_at'):
                setattr(i, 'last_at', arrow.utcnow())

        except TypeError:
            i = None

        return i

    def __dict__(self):
        s = str(self)
        return json.loads(s)

    def _format_fields(self):
        i = {}
        for k in FIELDS:

            v = getattr(self, k)
            if not v and k == 'confidence':
                i[k] = 0.0

                continue

            if not v:
                continue

            if k == 'confidence':
                v = float(v)

            elif k in FIELDS_TIME and isinstance(v, datetime):
                v = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            elif k == 'message':
                v = b64encode(v.encode('utf-8')).decode('utf-8')

            else:
                if isinstance(v, BASESTRING):
                    v = v.lower()

            i[k] = v

        return i

    # https://stackoverflow.com/questions/48991911/how-to-write-a-custom-json-decoder-for-a-complex-object
    def __repr__(self):
        i = self._format_fields()

        sort_keys = False
        indent = None
        if logging.getLogger('').getEffectiveLevel() == logging.DEBUG:
            sort_keys = True
            indent = 4

        return json.dumps(i, indent=indent, sort_keys=sort_keys,
                          separators=(',', ': '))

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
             Env Variables:
                CSIRTG_INDICATOR_TLP
                CSIRTG_INDICATOR_GROUP

            example usage:
                $ csirtg-indicator -d
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-indicator'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('-V', '--version', action='version', version=VERSION)

    p.add_argument('--group', help="specify group")
    p.add_argument('--indicator', '-i', help="specify indicator")
    p.add_argument('--tlp', help='specify tlp', default='green')
    p.add_argument('--tags', help='specify tags')

    args = p.parse_args()

    loglevel = logging.getLevelName('INFO')

    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    i = Indicator(indicator=args.indicator, tlp=args.tlp, tags=args.tags)
    i.geo_resolve()

    print(i)


if __name__ == '__main__':
    main()
