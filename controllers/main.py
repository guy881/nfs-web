from cgi import FieldStorage

import os
from weppy import request

from app import app
from utils import generate_unique_filename


@app.route("/")
def index():
    return '"Willkommen! And bienvenue! Welcome!"'


@app.route("/file-upload")
def file_upload():
    fileitem = request.params['file']
    if isinstance(fileitem, FieldStorage) and fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        filepath = f'media/{filename}'
        while os.path.isfile(filepath):  # if file exist don't override it, use different filename
            filename = generate_unique_filename(filename)
            filepath = f'media/{filename}'
        open(filepath, 'wb').write(fileitem.file.read())
        return filename
    else:
        return "erorr!"


@app.route('/<any:p>', methods='options')
def _options(p):
    """
    Required for CORS's preflighted requests
    """
    return ""
