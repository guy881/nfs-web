from app import app


@app.route("/")
def index():
    return '"Willkommen! And bienvenue! Welcome!"'
