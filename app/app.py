from datetime import timedelta
from functools import wraps
from os import getenv

from flask import Flask, Response
from flask_jwt_extended import JWTManager

app = Flask(__name__)
JWTManager(app)

app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=30)

app.config["GENERAL_SERVER_ERROR"] = "Unknown Server Error"

# Routes need to be imported after Flask app was initiated
import routes


def json_response(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return inner_func
