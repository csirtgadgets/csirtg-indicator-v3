from csirtg_geo import get


class Geo(object):
    def geo_resolve(self):
        rv = get(self.indicator)
        if not rv:
            if self.rdata:
                rv = get(self.rdata[0])

            else:
                return

        for k, v in rv.items():
            setattr(self, k, v)

