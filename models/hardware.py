from weppy.orm import Model, Field, belongs_to, has_many, before_update, before_insert


class SpectrumAnalyzer(Model):
    tablename = 'SpectrumAnalyzers'
    has_many(
        {'probes': 'FieldProbe'},
        {'scans': 'Scan'}
    )
    name = Field.string()
    model = Field.string()
    min_frequency = Field.float()
    max_frequency = Field.float()
    min_frequency_unit = Field.string(default='GHz')
    max_frequency_unit = Field.string(default='GHz')
    default = Field.bool()

    validation = {
        "name": {'presence': True},
        "model": {'presence': True},
        "min_frequency": {'presence': True},
        "max_frequency": {'presence': True},
    }

    default_values = {
        'default': False
    }

    indexes = {
        'name_index': {
            'fields': ['name'],
            'unique': True
        }
    }

    @before_update
    def set_as_default(self, dbset, fields):
        self._set_as_default(fields)

    @before_insert
    def set_new_as_default(self, fields):
        self._set_as_default(fields)

    @staticmethod
    def _set_as_default(fields):
        if fields['default']:
            analyzers = SpectrumAnalyzer.where(lambda s: (s.default == True)).select()
            for analyzer in analyzers:
                analyzer.update_record(default=False)


class FieldProbe(Model):
    tablename = 'FieldProbes'
    name = Field.string()
    kind = Field.string()
    min_frequency = Field.float()
    max_frequency = Field.float()
    min_frequency_unit = Field.string(default='GHz')
    max_frequency_unit = Field.string(default='GHz')
    correction_factor = Field.string()  # filename
    default = Field.bool()

    validation = {
        "name": {'presence': True},
        "kind": {'presence': True, 'in': ('e', 'h')},
        "min_frequency": {'presence': True},
        "max_frequency": {'presence': True},
        "correction_factor": {'allow': 'empty'},
    }

    repr_values = {
        'kind': lambda kind: {'e': 'E', 'h': 'H'}.get(kind)
    }

    default_values = {
        'default': False,
        'correction_factor': 1
    }

    indexes = {
        'name_index': {
            'fields': ['name'],
            'unique': True
        }
    }

    @before_update
    def set_as_default(self, dbset, fields):
        self._set_as_default(fields)

    @before_insert
    def set_new_as_default(self, fields):
        self._set_as_default(fields)

    @staticmethod
    def _set_as_default(fields):
        if fields['default']:
            probes = FieldProbe.where(lambda s: (s.default == True)).select()
            for probe in probes:
                probe.update_record(default=False)
