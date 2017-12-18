from weppy import Pipe, response


class CORS(Pipe):
    def open(self):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, PATCH, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization"
