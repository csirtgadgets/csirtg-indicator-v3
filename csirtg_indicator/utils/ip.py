import ipaddress
import socket
import re

from csirtg_indicator.constants import RE_IPV4, RE_IPV4_CIDR


def _test_socket(s, version=socket.AF_INET):
    try:
        socket.inet_pton(version, s)
        return True

    except socket.error:
        return None

    except UnicodeEncodeError:
        return False


def is_ip(i):
    return is_ipv4(i) or is_ipv6(i)


def is_ipv6(s):
    r = _test_socket(s, socket.AF_INET6)
    if r in [True, False]:
        return r

    try:
        ipaddress.IPv6Network(s, strict=False)
        return True
    except ipaddress.AddressValueError:
        pass


def is_ipv4(s):
    r = _test_socket(s)
    if r in [True, False]:
        return r

    if re.match(RE_IPV4, s):
        return True


def is_ipv4_net(s):
    if not re.match(RE_IPV4_CIDR, s):
        return False

    try:
        ipaddress.ip_network(s, strict=False)
        return True
    except ValueError as e:
        return False
