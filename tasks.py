from time import sleep

import scipy.io
from celery import Celery
from weppy import App
from weppy.orm import Database

from models.hardware import FieldProbe, SpectrumAnalyzer
from models.scanning import Scan, ScanResult

celer = Celery('tasks', broker='pyamqp://guest@localhost//')


def initialize_database():
    app = App('app')
    app.config_from_yaml('db.yml', 'db')
    db = Database(app)
    db.define_models(SpectrumAnalyzer, FieldProbe, Scan, ScanResult)
    return db


def save_scan_result(scan):
    mat_contents = scipy.io.loadmat('data/NFS.mat')

    x = mat_contents['x'].flatten()
    y = mat_contents['y'].flatten()
    z = mat_contents['z'].flatten()
    f = mat_contents['f'].flatten()
    e = mat_contents['E']

    scipy.set_printoptions(threshold=scipy.inf)
    kwargs = {'formatter': {'float_kind': lambda number: "%.3f" % number}, 'separator': ', '}
    x = scipy.array2string(x, **kwargs)
    y = scipy.array2string(y, **kwargs)
    z = scipy.array2string(z, **kwargs)
    f = scipy.array2string(f, **kwargs)
    e = scipy.array2string(e, **kwargs)

    result = ScanResult.create(x=x, y=y, z=z, f=f, e=e, scan=scan.id)
    scan.update_record(status='finished')
    print(result)


@celer.task
def increase_progress(scan_id):
    db = initialize_database()
    with db.connection():
        scan = Scan.get(scan_id)
        while scan.progress != 80:
            scan.update_record(progress=scan.progress + 10)
            db.commit()
            sleep(1)

        save_scan_result(scan)
        scan.update_record(progress=100)
        db.commit()
