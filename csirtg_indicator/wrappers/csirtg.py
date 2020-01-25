
class Csirtg(object):
    def csirtg(self):
        try:
            from csirtgsdk.client import Client
            from csirtgsdk.search import Search
        except ImportError:
            print('')
            print('The csirtg function requires the csirtgsdk')
            print('$ pip install csirtgsdk')
            print('$ export CSIRTG_TOKEN=1234...')
            print('')
            raise SystemExit

        return Search(Client()).search(self.indicator, limit=5)
