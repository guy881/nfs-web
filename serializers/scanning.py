import scipy.io
from weppy_rest import Serializer

from models.scanning import Scan


class ScanSerializer(Serializer):
    attributes = ['id', 'name', 'date', 'kind', 'min_frequency', 'max_frequency', 'analyzer', 'min_frequency_unit',
                  'max_frequency_unit', 'pcb_filename', 'status', 'progress', 'min_z', 'max_z']

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

    def z_availabe(self, row):
        return row.kind in ['volumetric', 'z']

    def result(self, row):
        result = row.result()
        return result.id if result else None


class ResultSerializer(Serializer):
    attributes = ['id', 'x_index', 'y']


class ScanResultMatSerializer(Serializer):
    attributes = ['id']

    def __serialize__(self, row, **extras):
        self.mat_contents = scipy.io.loadmat('data/{}'.format(row.mat_filename))
        return super().__serialize__(row, **extras)

    def x(self, row):
        x = self.mat_contents['x'].flatten()
        return x.tolist()

    def y(self, row):
        y = self.mat_contents['y'].flatten()
        return y.tolist()

    def z(self, row):
        z = self.mat_contents['z'].flatten()
        return z.tolist()

    def f(self, row):
        f = self.mat_contents['f'].flatten()
        return f.tolist()

    def e(self, row):
        e = self.mat_contents['E']
        return e.tolist()

