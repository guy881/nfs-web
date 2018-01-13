from weppy_rest import Serializer

from models.scanning import Scan


class ScanSerializer(Serializer):
    attributes = ['id', 'name', 'date', 'kind', 'min_frequency', 'max_frequency', 'analyzer', 'min_frequency_unit',
                  'max_frequency_unit', 'pcb_filename', 'status', 'progress']

    def freq_range(self, row):
        return f"{row.min_frequency} {row.min_frequency_unit} - {row.max_frequency} {row.max_frequency_unit}"

    def printable_date(self, row):
        return Scan.date.represent(row.date)

    def printable_kind(self, row):
        return Scan.kind.represent(row.kind)

    def analyzer_name(self, row):
        return row.analyzer.name if row.analyzer else ''

    def probe_name(self, row):
        return row.probe.name if row.probe else ''
