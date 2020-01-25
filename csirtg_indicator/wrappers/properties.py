from datetime import datetime
from csirtg_dt import get as get_dt
from csirtg_indicator.utils import resolve_itype, ipv4_normalize
from urllib.parse import urlparse

from csirtg_indicator.utils.confidence import estimate_confidence


class PropertiesMixin(object):

    @staticmethod
    def _time_setter(v):
        if not v:
            return

        if isinstance(v, datetime):
            return v
        else:
            return get_dt(v).to('utc').datetime

    @property
    def indicator(self):
        return self.__indicator

    @indicator.setter
    def indicator(self, i):
        if not i:
            self._indicator = None
            return

        i = i.lower()
        self.itype = resolve_itype(i)
        self._indicator = i

        if self.itype == 'url':
            u = urlparse(self._indicator)
            self._indicator = u.geturl().rstrip('/').lower()

        if self.itype == 'ipv4':
            self._indicator = ipv4_normalize(self._indicator)

        if self.mask and (self.itype in ['ipv4', 'ipv6']):
            self._indicator = '{}/{}'.format(self._indicator, int(self.mask))
            self.mask = None

    @indicator.getter
    def indicator(self):
        return self._indicator

    @property
    def asn_desc(self):
        return self._asn_desc

    @asn_desc.setter
    def asn_desc(self, v):
        if not v:
            self._asn_desc = None
            return

        if isinstance(v, str):
            self._asn_desc = v
            return

        try:
            self._asn_desc = v.decode('utf-8')
            return
        except UnicodeDecodeError:
            pass

        try:
            self._asn_desc = v.decode('latin-8')
            return
        except UnicodeDecodeError as e:
            raise e

    @asn_desc.getter
    def asn_desc(self):
        return self._asn_desc

    @property
    def confidence(self):
        return self._confidence

    @property
    def reported_at(self):
        return self._reported_at

    @reported_at.getter
    def reported_at(self):
        return self._reported_at

    @reported_at.setter
    def reported_at(self, v):
        self._reported_at = self._time_setter(v)

    @property
    def last_at(self):
        return self._last_at

    @last_at.getter
    def last_at(self):
        return self._last_at

    @last_at.setter
    def last_at(self, v):
        self._last_at = self._time_setter(v)

    @property
    def first_at(self):
        return self._first_at

    @first_at.getter
    def first_at(self):
        return self._first_at

    @first_at.setter
    def first_at(self, v):
        self._first_at = self._time_setter(v)

    @confidence.setter
    def confidence(self, v):
        if v is not None:
            self._confidence = float(v)
        else:
            self._confidence = None

    @confidence.getter
    def confidence(self):
        if self._confidence is None:
            return estimate_confidence(self)
        return self._confidence

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, v):
        self._count = int(v)

    @count.getter
    def count(self):
        return self._count

    def get(self, v, default=None):
        v1 = getattr(self, v)
        if v1:
            return v1
        return default
