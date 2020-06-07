import socket
import dns.resolver
from dns.resolver import NoAnswer, NXDOMAIN, NoNameservers, Timeout
from dns.name import EmptyLabel

from urllib.parse import urlparse

TIMEOUT = 5


def resolve_fqdn(host):
    if not host:
        return

    try:
        host = socket.gethostbyname(host)
        return host
    except Exception as e:
        return


def resolve_url(url):
    u = urlparse(url)
    return u.hostname


def resolve_ns(data, t='A', timeout=TIMEOUT, nameserver=None):
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    resolver.search = []

    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answers = resolver.query(data, t)

    except (NoAnswer, NXDOMAIN, EmptyLabel, NoNameservers, Timeout) as e:
        e = str(e)
        if e.startswith('The DNS operation timed out after'):
            return

        if 'The DNS response does not contain' in e or \
                'None of DNS query names exist' in e:
            return

        if 'failed to answer' in e:
            return

        raise

    resp = []
    for rdata in answers:
        resp.append(str(rdata))

    return resp