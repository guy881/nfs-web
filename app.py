from weppy import App
from weppy.orm import Database
from weppy_bs3 import BS3
from weppy_rest import REST

from utils import CORS

app = App(__name__)
app.config.url_default_namespace = "main"
app.use_extension(BS3)
app.use_extension(REST)

db = Database(app, auto_migrate=True)
app.pipeline = [db.pipe, CORS()]

from models.hardware import SpectrumAnalyzer, FieldProbe

db.define_models(SpectrumAnalyzer, FieldProbe)
from controllers import main, hardware

analyzers = app.rest_module(__name__, 'spectrumanalyzer', SpectrumAnalyzer, url_prefix='analyzers')
probes = app.rest_module(__name__, 'fieldprobe', FieldProbe, url_prefix='probes')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
