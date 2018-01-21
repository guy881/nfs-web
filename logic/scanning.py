from time import sleep

import psycopg2
import scipy.io
from weppy import App
from weppy.orm import Database

from models.hardware import FieldProbe, SpectrumAnalyzer
from models.scanning import Scan, ScanResult

app = App('app')
app.config_from_yaml('db.yml', 'db')
db = Database(app)
db.define_models(SpectrumAnalyzer, FieldProbe, Scan, ScanResult)


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
        return scan_id


def scan_finished_callback(scan_id):
    print("scan finished")
    mat_contents = scipy.io.loadmat('/home/stevens/Desktop/praca_inż/materiały/wizualizacja/NFS.mat')

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

    with db.connection():
        result = ScanResult.create(
            x=x,
            y=y,
            z=z,
            f=f,
            e=e,
            scan=scan_id
        )
        db.commit()


