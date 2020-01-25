import os

FIELDS_CORE = [
    'indicator', 'itype', 'tlp', 'provider', 'group', 'tlp', 'provider',
    'count', 'message', 'tags', 'confidence', 'description', 'version',
    'uuid', 'iid', 'oid', 'extra', 'comment', 'organization', 'brand'
]

FIELDS_TIME = [
    'first_at', 'last_at', 'reported_at'
]

FIELDS_META = [
    'application', 'reference', 'reference_tlp', 'data'
]

FIELDS_GEO = [
    'cc', 'latitude', 'timezone', 'longitude', 'city', 'region'
]

FIELDS_IP = [
    'portlist', 'protocol', 'dest', 'dest_portlist', 'mask',
    'rdata', 'rtype'
]

FIELDS_FQDN = [
    'ns', 'mx', 'cname'
]

FIELDS_SCORE = [
    'risk', 'score'
]

FIELDS_GRAPH = [
    'iid', 'oid'
]

FIELDS_ASN = [
    'asn', 'asn_desc', 'asn_created_at', 'prefix', 'asn_type', 'peers',
    'upstream', 'downstream'
]

FIELDS = FIELDS_CORE + FIELDS_GEO + FIELDS_META + FIELDS_IP + FIELDS_TIME \
         + FIELDS_FQDN + FIELDS_ASN + FIELDS_GRAPH + FIELDS_SCORE
