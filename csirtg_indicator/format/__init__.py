from .bind import get_lines as get_lines_bind
from .bindrpz import get_lines as get_lines_bindrpz
from .bro import get_lines as get_lines_bro
from .csv import get_lines as get_lines_csv
from .json import get_lines as get_lines_json
from .snort import get_lines as get_lines_snort
from .table import get_lines as get_lines_table
from .gexf import get_lines as get_lines_gexf


FORMATS = {
    'bind': get_lines_bind,
    'bindrpz': get_lines_bindrpz,
    'bro': get_lines_bro,
    'csv': get_lines_csv,
    'json': get_lines_json,
    'snort': get_lines_snort,
    'table': get_lines_table,
    'gexf': get_lines_gexf,
}
