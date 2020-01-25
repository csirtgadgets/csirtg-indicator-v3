import arrow
from csirtg_spamhaus import get


class Spamhaus(object):

    def spamhaus(self):

        if self.itype not in ['ipv4', 'ipv6']:
            return

        rv = get(self.indicator)
        if not rv:
            return

        confidence = 4
        if self.is_ip:
            ref = f"http://www.spamhaus.org/query/bl?ip={self.indicator}"

        else:
            if ' legit ' in rv['description']:
                confidence = 1

            ref = f"http://www.spamhaus.org/query/dbl?domain={self.indicator}"

        i = self.copy(**{
            'tags': rv['tags'],
            'description': rv['description'],
            'confidence': confidence,
            'provider': 'spamhaus.org',
            'reference': ref,
            'reference_tlp': 'white',
            'last_at': arrow.utcnow(),
        })

        if self.resolve_geo:
            i.geo_resolve()

        return i
