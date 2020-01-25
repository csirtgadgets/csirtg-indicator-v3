

class Farsight(object):

    def farsight(self):
        if self.itype != 'ipv4':
            raise TypeError('%s is not supported' % self.itype)

        try:
            from csirtg_dnsdb.client import Client
        except ImportError:
            print('')
            print('The csirtg function requires the csirtg_dnsdb client')
            print('https://github.com/csirtgadgets/dnsdb-py')
            print('$ pip install csirtg_dnsdb')
            print('$ export FARSIGHT_TOKEN=1234...')
            print('')
            raise SystemExit

        return Client().search(self.indicator)
