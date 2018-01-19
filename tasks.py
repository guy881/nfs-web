# from time import sleep
#
# from celery import Celery
# from weppy import App
# from weppy.orm import Database
#
# from models.hardware import FieldProbe, SpectrumAnalyzer
# from models.scanning import Scan
#
# celer = Celery('tasks', backend='db+sqlite:///databases/dummy.db', broker='pyamqp://guest@localhost//')
# app = App('app')
# app.config_from_yaml('db.yml', 'db')
# db = Database(app)
# db.define_models(SpectrumAnalyzer, FieldProbe, Scan)
#
#
# @celer.task
# def increase_progress(scan_id):
#     with db.connection():
#         scan = Scan.get(scan_id)
#         while scan.status != 'finished':
#             scan.update_record(progress=scan.progress + 10)
#             if scan.progress == 100:
#                 scan.update_record(status='finished')
#             sleep(2)
#             db.commit()
#         return scan
