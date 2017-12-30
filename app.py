from datetime import datetime

from weppy import App
from weppy.orm import Database
from weppy_bs3 import BS3
from weppy_rest import REST

from serializers.hardware import SpectrumAnalyzerSerializer, FieldProbeSerializer
from serializers.scanning import ScanSerializer
from utils import CORS

app = App(__name__)
app.config.url_default_namespace = "main"
app.use_extension(BS3)
app.use_extension(REST)

db = Database(app, auto_migrate=True)
app.pipeline = [db.pipe, CORS()]

from models.hardware import SpectrumAnalyzer, FieldProbe
from models.scanning import Scan

db.define_models(SpectrumAnalyzer, FieldProbe, Scan)
from controllers import main, hardware

analyzers = app.rest_module(__name__, 'spectrumanalyzer', SpectrumAnalyzer, serializer=SpectrumAnalyzerSerializer,
                            url_prefix='analyzers')
probes = app.rest_module(__name__, 'fieldprobe', FieldProbe, serializer=FieldProbeSerializer, url_prefix='probes')

scans = app.rest_module(__name__, 'scan', Scan, serializer=ScanSerializer, url_prefix='scans')


@scans.index()
def scans_list(dbset):
    rows = dbset.select(paginate=scans.get_pagination())
    response = scans.serialize_many(rows)
    response['next_scan_name'] = "Scan {}".format(Scan.all().count() + 1)  # name for new scan
    today = datetime.today()
    response['current_date'] = today
    response['current_date_printable'] = today.strftime("%d.%m.%Y")  # date for new scan
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
