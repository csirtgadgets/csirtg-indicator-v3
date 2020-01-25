from csirtg_indicator.constants import V4_RESERVED, V6_RESERVED
from csirtg_indicator.utils import is_subdomain
from csirtg_indicator.utils import url_to_fqdn


class ItypesMixin(object):
    itype = None
    indicator = None

    @property
    def is_fqdn(self):
        if self.itype == 'fqdn':
            return True

    @property
    def is_ip(self):
        if self.itype in ['ipv4', 'ipv6']:
            return True

    @property
    def is_ipv4(self):
        if self.itype == 'ipv4':
            return True

    @property
    def is_ipv6(self):
        if self.itype == 'ipv6':
            return True

    @property
    def is_url(self):
        if self.itype == 'url':
            return True

    @property
    def is_hash(self):
        if self.itype in ['md5', 'sha1', 'sha256', 'sha512']:
            return True

    @property
    def is_email(self):
        if self.itype == 'email':
            return True

    @property
    def is_private(self):
        if not self.itype:
            return False

        if not self.is_ip:
            return False

        if self.is_ipv4 and V4_RESERVED.get(str(self.indicator)):
            return True

        if self.is_ipv6 and V6_RESERVED.get(str(self.indicator)):
            return True

    @property
    def is_subdomain(self):
        return is_subdomain(self.indicator)

    @property
    def fqdn(self):
        if self.itype == 'fqdn':
            return self.indicator

        if self.itype != 'url':
            return

        return url_to_fqdn(self.indicator)

    def ipv4_to_prefix(self, n=24):
        prefix = self.indicator.split('.')
        prefix = prefix[:3]
        prefix.append('0/%i' % n)
        return '.'.join(prefix)
