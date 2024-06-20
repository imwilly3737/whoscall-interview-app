import logging
from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app.app import app
from app.utils import json_response
from model.user import user_records

logger = logging.getLogger(__name__)


@app.route("/login", endpoint="login", methods=["POST"])
@json_response
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        if not user_records.query_user(username, password):
            return jsonify(error='Invalid username or password'), HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    except Exception as ex:
        logger.exception("Exception when login: %r", ex)
        return jsonify(error=app.config["GENERAL_SERVER_ERROR"]), HTTPStatus.INTERNAL_SERVER_ERROR
