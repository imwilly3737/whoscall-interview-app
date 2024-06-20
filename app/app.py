from datetime import timedelta
from os import getenv

from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
JWTManager(app)

app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=30)

app.config["GENERAL_SERVER_ERROR"] = "Unknown Server Error"

# Routes need to be imported after Flask app was initiated
import routes
