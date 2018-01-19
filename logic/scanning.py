from time import sleep

import psycopg2
from weppy import App
from weppy.orm import Database

from models.hardware import FieldProbe, SpectrumAnalyzer
from models.scanning import Scan

app = App('app')
app.config_from_yaml('db.yml', 'db')
db = Database(app)
db.define_models(SpectrumAnalyzer, FieldProbe, Scan)


def begin_scan(scan_id):
    with db.connection():
        scan = None
        while not scan or scan.status != 'finished':
            if not scan:
                try:
                    scan = Scan.get(scan_id)
                except psycopg2.ProgrammingError:  # opened transaction or something, cannot fetch right now, try later
                    pass
            scan.update_record(progress=scan.progress + 10)
            if scan.progress == 100:
                scan.update_record(status='finished')
            db.commit()
            sleep(2)
        return scan


def scan_finished_callback(scan):
    print("scan finished", scan)
