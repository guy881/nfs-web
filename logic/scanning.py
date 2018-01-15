from time import sleep
from models.scanning import Scan


def begin_scan(scan_id):
    from app import db
    scan = Scan.get(scan_id)
    print(scan)
    while scan.status != 'finished':
        scan.update_record(progress=scan.progress + 10)
        print()
        if scan.progress == 100:
            scan.update_record(status='finished')
        db.commit()
        sleep(2)
    return scan


def scan_finished_callback(scan):
    print("scan finished", scan)