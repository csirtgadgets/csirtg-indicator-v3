
import logging
ENABLED = True

try:
    from csirtg_geo import get

except (ImportError, FileNotFoundError) as e:
    ENABLED = False

logger = logging.getLogger(__name__)


class Geo(object):
    def geo_resolve(self):
        if not ENABLED:
            logger.error('maxmind data/libraries not installed')
            return

        rv = get(self.indicator)
        if not rv and self.rdata:
            try:
                rv = get(self.rdata[0])

            except Exception as e:
                print(e)

        if not rv:
            return

        for k, v in rv.items():
            setattr(self, k, v)
