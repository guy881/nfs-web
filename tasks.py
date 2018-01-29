from time import sleep

import os
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


def save_scan_result(scan_id):
    x_set, y_set, z_set, f_set = (set() for i in range(4))  # multiple sets
    e_list = []

    dir_path = 'data/{}'.format(scan_id)
    files = os.listdir(dir_path)
    for filename in files:
        mesurement_no, coords_and_extension = filename.split('-')
        coords = coords_and_extension[:-4]
        x, y, z = [int(coord) for coord in coords.split('_')]
        x_set.add(x)
        y_set.add(y)
        z_set.add(z)
        f = open(os.path.join(dir_path, filename))
        lines = f.readlines()[28:]
        for line in lines:
            frequency, max_e, min_e = [float(num) for num in line.split(';')]
            f_set.add(frequency)
            e_list.append({'x': x, 'y': y, 'z': z, 'f': frequency, 'e': max_e})
        f.close()

    e_sci = scipy.zeros((len(x_set), len(y_set), len(z_set), len(f_set)))  # destined 4 dimensional E matrix
    xs = sorted(x_set)
    ys = sorted(y_set)
    zs = sorted(z_set)
    fs = sorted(f_set)
    for e in e_list:
        x_index = xs.index(e['x'])
        y_index = ys.index(e['y'])
        z_index = zs.index(e['z'])
        f_index = fs.index(e['f'])
        e_sci[x_index, y_index, z_index, f_index] = e['e']

    output_dict = {'x': xs, 'y': ys, 'z': zs, 'f': fs, 'E': e_sci}
    mat_file = '{}.mat'.format(scan_id)
    scipy.io.savemat('data/{}'.format(mat_file), output_dict)

    # Here should be code for parsing data from spectrum analyzer and saving it as .mat file
    db = initialize_database()
    with db.connection:
        ScanResultMat.create(mat_filename=mat_file, scan=scan_id)
        db.commit()


class ScanerObserver():

    def __init__(self, scan_id):
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
    scan_observer = ScanerObserver(scan_id)
    nfs = skaner.NFS(observer=scan_observer)
    nfs.scan('emc_scanner/rpi0_res10.gcode', scan_id=scan_id)
    save_scan_result(scan_id)
