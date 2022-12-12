from app import app
from werkzeug.exceptions import HTTPException
from app.controllers.helpers import apology

@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return apology(e.name, e.code)