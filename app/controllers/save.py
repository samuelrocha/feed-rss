from app import app
from flask import redirect, request
from datetime import datetime
from flask_login import current_user, login_required

@app.get('/save')
@login_required
def get_save():
        
    return "SAFE "