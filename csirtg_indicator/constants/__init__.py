import os

from csirtg_re import *
from .fields import FIELDS, FIELDS_TIME
from .networks import V4_RESERVED, V6_RESERVED

VERSION = '3.0a0'

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

COLUMNS = ['tlp', 'group', 'reported_at', 'indicator', 'risk', 'asn', 'cc',
           'first_at', 'last_at', 'count', 'tags', 'description', 'confidence',
           'provider', 'reference']

MAX_FIELD_SIZE = 30

BASESTRING = (str, bytes)

GEO = False
if os.getenv('CSIRTG_INDICATOR_GEO', '') == '1':
    GEO = True

PEERS = False
if os.getenv('CSIRTG_INDICATOR_PEERS', '') == '1':
    PEERS = True

FQDN = False
if os.getenv('CSIRTG_INDICATOR_FQDN', '') == '1':
    FQDN = True
