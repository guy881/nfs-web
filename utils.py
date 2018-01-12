from random import randrange
from weppy import Pipe, response


class CORS(Pipe):
    def open(self):
        allow_headers = ["Origin", "Content-Type", "Accept", "Authorization", "Cache-Control", "X-Requested-With"]
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, PATCH, DELETE"
        response.headers["Access-Control-Allow-Headers"] = ', '.join(allow_headers)


def generate_unique_filename(filename):
    dot = filename.rfind('.')
    name = filename[:dot]
    extension = filename[dot:]
    suffix = randrange(1000000)
    return f'{name}_{suffix}{extension}'
