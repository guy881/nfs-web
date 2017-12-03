from weppy.tools import service

from app import app
from models.hardware import SpectrumAnalyzer


# @app.route("analyzers")
# @service.json
# def spectrum_analyzers_list():
#     print("hey")
#     analyzers = SpectrumAnalyzer.all()
#     return analyzers
