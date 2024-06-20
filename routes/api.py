from http import HTTPStatus
import logging

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.app import app
from app.utils import json_response
from model.tasks import task_records


logger = logging.getLogger(__name__)


@app.route("/health_check", endpoint="health_check")
@json_response
def health_check():
    return "OK"


@app.route("/tasks", endpoint="get_tasks")
@jwt_required()
@json_response
def get_tasks():
    try:
        return jsonify(result=task_records.query())
    except Exception as ex:
        logger.exception("Exception when getting tasks: %r", ex)
        return jsonify(error=app.config["GENERAL_SERVER_ERROR"]), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task", endpoint="add_task", methods=['POST'])
@jwt_required()
@json_response
def add_task():
    try:
        data = request.get_json()
        if "name" not in data:
            return jsonify(error="name field is not provided"), HTTPStatus.BAD_REQUEST
        return jsonify(result=task_records.add(name=data["name"])), HTTPStatus.CREATED
    except Exception as ex:
        logger.exception("Exception when adding task: %r", ex)
        return jsonify(error=app.config["GENERAL_SERVER_ERROR"]), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task/<int:t_id>", endpoint="update_task", methods=['PUT'])
@jwt_required()
@json_response
def update_task(t_id: int):
    try:
        data = request.get_json()
        return jsonify(result=task_records.update(t_id, data))
    except KeyError:
        return jsonify(error="id does not exist"), HTTPStatus.NOT_FOUND
    except Exception as ex:
        logger.exception("Exception when updating task: %r", ex)
        return jsonify(error=app.config["GENERAL_SERVER_ERROR"]), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task/<int:t_id>", endpoint="delete_task", methods=['DELETE'])
@jwt_required()
@json_response
def delete_task(t_id: int):
    try:
        task_records.delete(t_id)
        return '', HTTPStatus.OK
    except KeyError:
        return jsonify(error="id does not exist"), HTTPStatus.NOT_FOUND
    except Exception as ex:
        logger.exception("Exception when updating task: %r", ex)
        return jsonify(error=app.config["GENERAL_SERVER_ERROR"]), HTTPStatus.INTERNAL_SERVER_ERROR
