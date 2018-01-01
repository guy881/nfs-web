from datetime import datetime

from weppy.orm import Model, Field, has_one, belongs_to


class Scan(Model):
    tablename = 'Scans'
    belongs_to({'analyzer': 'SpectrumAnalyzer'})
    belongs_to({'probe': 'FieldProbe'})
    name = Field.string()
    date = Field.datetime()
    kind = Field.string()
    min_frequency = Field.float()
    max_frequency = Field.float()

    validation = {
        'name': {'presence': True},
        'kind': {'presence': True, 'in': ('flat', 'volumetric', 'z')},
        'min_frequency': {'presence': True},
        'max_frequency': {'presence': True},
    }

    repr_values = {
        'kind': lambda kind: {'flat': 'Flat', 'volumetric': 'Volumetric', 'z': 'Z-variable'}.get(kind),
        'date': lambda date: date.strftime("%d.%m.%Y")
    }

    default_values = {
        'date': lambda: datetime.now
    }

    indexes = {
        'name_index': {
            'fields': ['name'],
            'unique': True
        }
    }
