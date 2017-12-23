from app import app


@app.route("/")
def index():
    return '"Willkommen! And bienvenue! Welcome!"'


@app.route('/<any:p>', methods='options')
def _options(p):
    """
    Required for CORS's preflighted requests
    """
    return ""
