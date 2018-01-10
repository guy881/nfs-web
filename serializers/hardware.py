from weppy_rest import Serializer


class SpectrumAnalyzerSerializer(Serializer):
    attributes = ['id', 'name', 'model', 'min_frequency', 'max_frequency', 'default', 'min_frequency_unit',
                  'max_frequency_unit']

    def freq_range(self, row):
        return f"{row.min_frequency} {row.min_frequency_unit} - {row.max_frequency} {row.max_frequency_unit}"


class FieldProbeSerializer(Serializer):
    attributes = ['id', 'name', 'kind', 'min_frequency', 'max_frequency', 'correction_factor', 'default',
                  'min_frequency_unit', 'max_frequency_unit']

    def freq_range(self, row):
        return f"{row.min_frequency} {row.min_frequency_unit} - {row.max_frequency} {row.max_frequency_unit}"
