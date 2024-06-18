from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from app.app import app
from model.user import User


@app.route("/login", endpoint="login", methods=["POST"])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not User.query_user(username, password):
        return jsonify(error='Invalid username or password'), HTTPStatus.UNAUTHORIZED
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh", endpoint="refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
