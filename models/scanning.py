from datetime import datetime

from weppy.orm import Model, Field, belongs_to, has_one, has_many


class Scan(Model):
    tablename = 'Scans'
    belongs_to({'analyzer': 'SpectrumAnalyzer'})
    belongs_to({'probe': 'FieldProbe'})
    has_one({'result_mat': 'ScanResultMat'})
    name = Field.string()
    date = Field.datetime()
    kind = Field.string()
    min_frequency = Field.float()
    max_frequency = Field.float()
    min_frequency_unit = Field.string(default='GHz')
    max_frequency_unit = Field.string(default='GHz')
    min_x = Field.float(validation={'blank': True, 'gte': 0})
    min_y = Field.float(validation={'blank': True, 'gte': 0})
    min_z = Field.float(validation={'blank': True, 'gte': 0})
    max_x = Field.float(validation={'blank': True, 'gt': 0})
    max_y = Field.float(validation={'blank': True, 'gt': 0})
    max_z = Field.float(validation={'blank': True, 'gt': 0})
    pcb_filename = Field.string(default='')
    status = Field.string()
    progress = Field.int(default=0)

    validation = {
        'name': {'presence': True},
        'kind': {'presence': True, 'in': ('flat', 'volumetric', 'z')},
        'min_frequency': {'presence': True, 'gt': 0},
        'max_frequency': {'presence': True, 'gt': 0},
    }

    repr_values = {
        'kind': lambda kind: {'flat': 'Flat', 'volumetric': 'Volumetric', 'z': 'Z-variable'}.get(kind),
        'date': lambda date: date.strftime("%d.%m.%Y")
    }

    default_values = {
        'date': lambda: datetime.now,
    }

    indexes = {
        'name_index': {
            'fields': ['name'],
            'unique': True
        }
    }


class ScanResult(Model):
    tablename = 'ScanResults'
    belongs_to({'scan': 'Scan'})
    has_many({'x_results': 'XResultRow'})
    x = Field.text()
    y = Field.text()
    z = Field.text()
    f = Field.text()
    e = Field.text(auto_validation=False)
    s = Field.blob()


class ScanResultMat(Model):
    tablename = 'ScanResultsMat'
    belongs_to({'scan': 'Scan'})
    mat_filename = Field.string(default='')


class XResultRow(Model):
    tablename = 'XResultRows'
    belongs_to({'result': 'ScanResult'})
    x_index = Field.int()
    y = Field.text(auto_validation=False)
