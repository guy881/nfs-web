from weppy_rest import Serializer


class SpectrumAnalyzerSerializer(Serializer):
    attributes = ['id', 'name', 'model', 'min_frequency', 'max_frequency', 'default']

    def freq_range(self, row):
        return "{} GHz - {} GHz".format(row.min_frequency, row.max_frequency)
