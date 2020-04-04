from csirtg_peers import get


class Peers(object):

    def peers_resolve(self):
        if self.is_private or not self.itype == 'ipv4':
            return

        self.peers = list(get(self.indicator))
