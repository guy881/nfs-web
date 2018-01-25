from datetime import datetime

from multiprocessing.pool import Pool
from weppy import App, response
from weppy.orm import Database
from weppy_bs3 import BS3
from weppy_rest import REST

from logic.scanning import begin_scan, scan_finished_callback
from serializers.hardware import SpectrumAnalyzerSerializer, FieldProbeSerializer
from serializers.scanning import ScanSerializer
from tasks import increase_progress
from utils import CORS

app = App(__name__)
app.config.url_default_namespace = "main"
app.use_extension(BS3)
app.use_extension(REST)

app.config_from_yaml('db.yml', 'db')
db = Database(app, auto_migrate=True)
app.pipeline = [db.pipe, CORS()]

from models.hardware import SpectrumAnalyzer, FieldProbe
from models.scanning import Scan, ScanResult

db.define_models(SpectrumAnalyzer, FieldProbe, Scan, ScanResult)
from controllers import main, hardware

analyzers = app.rest_module(__name__, 'spectrumanalyzer', SpectrumAnalyzer, serializer=SpectrumAnalyzerSerializer,
                            url_prefix='analyzers')
probes = app.rest_module(__name__, 'fieldprobe', FieldProbe, serializer=FieldProbeSerializer, url_prefix='probes')

scans = app.rest_module(__name__, 'scan', Scan, serializer=ScanSerializer, url_prefix='scans')

results = app.rest_module(__name__, 'result', ScanResult, url_prefix='results')


@scans.index()
def scans_list(dbset):
    rows = dbset.select(paginate=scans.get_pagination())
    response = scans.serialize_many(rows)
    last = Scan.last()
    new_id = last.id + 1 if last else 1
    response['next_scan_name'] = "Scan {}".format(new_id)  # name for new scan
    today = datetime.today()
    response['current_date'] = today
    response['current_date_printable'] = today.strftime("%d.%m.%Y")  # date for new scan
    return response


@scans.create()
def scans_new():
    attrs = scans.parse_params()
    resp = Scan.create(**attrs)
    if resp.errors:
        response.status = 422
        return scans.error_422(resp.errors)

    # success, proceed with scan
    serialized_scan = scans.serialize_one(resp.id)
    async_result = increase_progress.delay(resp.id)
    # pool = Pool()
    # pool.apply_async(begin_scan, args=[resp.id], callback=scan_finished_callback)
    # pool.close()

    return serialized_scan


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
