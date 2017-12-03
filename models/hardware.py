from weppy.orm import Model, Field, belongs_to, has_many


class SpectrumAnalyzer(Model):
    tablename = 'SpectrumAnalyzers'
    has_many({'probes': 'FieldProbe'})
    name = Field.string()
    model = Field.string()
    min_frequency = Field.float()
    max_frequency = Field.float()
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


class FieldProbe(Model):
    tablename = 'FieldProbes'
    belongs_to({'analyzer': 'SpectrumAnalyzer'})
    name = Field.string(validation={'presence': True})
    kind = Field.string(validation={'presence': True, 'in': ('e', 'h')})
    min_frequency = Field.float(validation={'presence': True})
    max_frequency = Field.float(validation={'presence': True})
    correction_factor = Field.float(validation={'allow': 'empty'}, default=1)
    default = Field.bool()

    repr_values = {
        'kind': lambda kind: {'e': 'E', 'h': 'H'}.get(kind)
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
