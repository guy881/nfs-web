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
    x = mat_contents['x'].flatten()
    y = mat_contents['y'].flatten()
    z = mat_contents['z'].flatten()
    f = mat_contents['f'].flatten()
    e = mat_contents['E']

    print(request.query_params)
    q = request.query_params
    start_z = int(q.get('sz', 0))
    end_z = int(q.get('ez', z.size - 1))
    start_f = int(q.get('sf', 0))
    end_f = int(q.get('ef', f.size - 1))

    sliced = e[:, :, start_z:end_z, start_f:end_f]

    reduced = scipy.add.reduce(sliced, axis=(2, 3,))

    return {
        'x': x.tolist(),
        'y': y.tolist(),
        'z': z.tolist(),
        'f': f.tolist(),
        'e': reduced.tolist()
    }
