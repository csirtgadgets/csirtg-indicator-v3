from csirtg_indicator.utils.fqdn import resolve_fqdn, resolve_ns, \
    resolve_url


class DNS(object):

    @staticmethod
    def _is_invalid(i):
        if not i:
            return True

        if i in ["", "localhost"]:
            return True

    def _set_rr(self, d, t='A'):
        r = resolve_ns(d, t=t)
        if self._is_invalid(r):
            return

        r = [str(rr) for rr in r]
        setattr(self, t.lower(), r)

    def fqdn_resolve(self):
        if self.itype not in ['url', 'fqdn']:
            return

        d = self.indicator
        if self.itype == 'url':
            d = resolve_url(self.indicator)
            if not d:
                return

        r = resolve_ns(d)
        if self._is_invalid(r):
            return

        if not isinstance(r, list):
            r = [r]

        setattr(self, 'rdata', r)
        setattr(self, 'rtype', 'A')

        for t in ['NS', 'MX', 'CNAME']:
            self._set_rr(d, t)
