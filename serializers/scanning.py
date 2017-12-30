from weppy_rest import Serializer


class ScanSerializer(Serializer):
    attributes = ['id', 'name', 'date', 'kind', 'min_frequency', 'max_frequency']

    def freq_range(self, row):
        return "{} GHz - {} GHz".format(row.min_frequency, row.max_frequency)
