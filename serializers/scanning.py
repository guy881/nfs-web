from weppy_rest import Serializer

from models.scanning import Scan


class ScanSerializer(Serializer):
    attributes = ['id', 'name', 'date', 'kind', 'min_frequency', 'max_frequency', 'analyzer']

    def freq_range(self, row):
        return "{} GHz - {} GHz".format(row.min_frequency, row.max_frequency)

    def printable_date(self, row):
        return Scan.date.represent(row.date)

    def printable_kind(self, row):
        return Scan.kind.represent(row.kind)

    def analyzer_name(self, row):
        return row.analyzer.name if row.analyzer else ''

    def probe_name(self, row):
        return row.probe.name if row.probe else ''
