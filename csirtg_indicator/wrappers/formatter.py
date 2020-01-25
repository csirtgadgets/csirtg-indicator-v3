

class FormatterMixin(object):
    def to_json(self):
        return str(self)

    def to_csv(self):
        from csirtg_indicator.format.csv import get_lines
        return next(get_lines([self]))

    def to_bro(self):
        from csirtg_indicator.format.bro import get_lines
        return next(get_lines([self]))

    def to_snort(self):
        from csirtg_indicator.format.snort import get_lines
        return next(get_lines([self]))

    def to_table(self):
        from csirtg_indicator.format.table import get_lines
        return next(get_lines([self]))

    def to_gexf(self):
        raise NotImplementedError('see: https://networkx.github.io/'
                                  'documentation/networkx-1.10/reference/'
                                  'readwrite.html')
