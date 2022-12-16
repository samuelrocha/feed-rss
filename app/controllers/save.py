from app import app
from flask import redirect, request
from datetime import datetime
from flask_login import current_user
from app.models.Feed import Feed

@app.get('/save')
def get_save():
        
    return "SAFE "