from time import sleep

import scipy.io
from celery import Celery
from weppy import App
from weppy.orm import Database
from emc_scanner import skaner

from models.hardware import FieldProbe, SpectrumAnalyzer
from models.scanning import Scan, ScanResult, XResultRow, ScanResultMat

celer = Celery('tasks', broker='pyamqp://guest@localhost//')


def initialize_database():
    app = App('app')
    app.config_from_yaml('db.yml', 'db')
    db = Database(app)
    db.define_models(SpectrumAnalyzer, FieldProbe, Scan, ScanResult, XResultRow, ScanResultMat)
    return db


def save_scan_result(scan):
    # Here should be code for parsing data from spectrum analyzer and saving it as .mat file
    sr = ScanResultMat.create(mat_filename='NFS.mat', scan=scan.id)
    print(sr)


class ScanerObserver():

    def __init__(self, scan_id) -> None:
        self.scan_id = scan_id
        super().__init__()

    def update_progress(self, progress, total):
        print("hello from observer")
        db = initialize_database()
        with db.connection():
            scan = Scan.get(self.scan_id)
            scan.update_record(progress=progress / total * 100)
            if progress == total:
                scan.update_record(status='finished')
            db.commit()


@celer.task
def increase_progress(scan_id):
    db = initialize_database()
    scan_observer = ScanerObserver(scan_id)
    nfs = skaner.NFS(observer=scan_observer)
    nfs.scan('emc_scanner/rpi0_res10.gcode', scan_id=scan_id)
    # with db.connection():
    #     scan = Scan.get(scan_id)
    #     while scan.progress != 80:
    #         scan.update_record(progress=scan.progress + 10)
    #         db.commit()
    #         sleep(1)
    #
    #     save_scan_result(scan)
    #     scan.update_record(progress=100, status='finished')
    #     db.commit()
