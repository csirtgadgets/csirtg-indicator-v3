import os

ENABLED = False
try:
    import networkx as nx
    ENABLED = True

except ImportError:
    pass

PATH = os.getenv('GEXF_PATH', 'indicators.gexf')


def get_lines(data, path=PATH):
    if not ENABLED:
        raise ImportError('missing networkx library')

    g = nx.Graph()

    if not isinstance(data, list):
        data = [data]

    for i in data:
        g.add_node(i['indicator'], itype=i['itype'])
        for a in ['cc']:
            if not i.get(a):
                continue

            g.add_node(i[a])
            g.add_edge(i['indicator'], i[a])

    nx.write_gexf(g, path, prettyprint=True)
    return ['Graph generated successfully: %s' % path]
