from time import sleep

import scipy.io
from celery import Celery
from weppy import App
from weppy.orm import Database

from models.hardware import FieldProbe, SpectrumAnalyzer
from models.scanning import Scan, ScanResult, XResultRow

celer = Celery('tasks', broker='pyamqp://guest@localhost//')


def initialize_database():
    app = App('app')
    app.config_from_yaml('db.yml', 'db')
    db = Database(app)
    db.define_models(SpectrumAnalyzer, FieldProbe, Scan, ScanResult, XResultRow)
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
    x_str = scipy.array2string(x, **kwargs)
    y_str = scipy.array2string(y, **kwargs)
    z_str = scipy.array2string(z, **kwargs)
    f_str = scipy.array2string(f, **kwargs)
    # e = scipy.array2string(e, **kwargs)

    result = ScanResult.create(x=x_str, y=y_str, z=z_str, f=f_str, scan=scan.id)
    for x_index, y in enumerate(e):
        y_str = scipy.array2string(y, **kwargs)
        XResultRow.create(x_index=x_index, y=y_str, result=result.id)

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
