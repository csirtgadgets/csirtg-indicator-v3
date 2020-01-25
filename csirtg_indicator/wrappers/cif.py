

class Cif(object):

    def cif(self):
        try:
            from cifsdk.client.http import HTTP as Client
        except ImportError:
            print('')
            print('The cif function requires the cifsdk>=4.0')
            print('$ pip install https://github.com/csirtgadgets/'
                  'verbose-robot-sdk-py/archive/master.zip')
            print('$ export CIF_TOKEN=1234...')
            print('')
            raise SystemExit

        return Client().search({'q': self.indicator, 'limit': 25})
