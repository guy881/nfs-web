import scipy.io
from weppy import request
from weppy.tools import service

from app import app
from models.scanning import ScanResultMat


@app.route("mtresults/<int:id>")
@service.json
def scan_result(id):
    result = ScanResultMat.get(id)
    mat_contents = scipy.io.loadmat('data/{}'.format(result.mat_filename))
    x = mat_contents['x'].flatten().tolist()
    y = mat_contents['y'].flatten().tolist()
    z = mat_contents['z'].flatten().tolist()
    f = mat_contents['f'].flatten().tolist()
    e = mat_contents['E']

    q = request.query_params
    start_z = int(q.get('sz', 0))
    end_z = int(q.get('ez', len(z) - 1))
    start_f = int(q.get('sf', 0))
    end_f = int(q.get('ef', len(f) - 1))

    sliced = e[:, :, start_z:end_z + 1, start_f:end_f + 1]
    print(x)

    reduced = scipy.add.reduce(sliced, axis=(2, 3,))

    return {
        'x': x,
        'y': y,
        'z': z,
        'f': f,
        'e': reduced.tolist()
    }
