from http import HTTPStatus
import logging

from flask import Flask, jsonify, request

from tasks.tasks import task_records

app = Flask(__name__)
logger = logging.getLogger(__name__)

GENERAL_SERVER_ERROR = "Unknown Server Error"


@app.route("/health_check")
def health_check():
    return "OK"


@app.route("/tasks")
def get_tasks():
    try:
        return jsonify({"result": task_records.query()})
    except Exception as ex:
        logger.exception("Exception when getting tasks: %r", ex)
        return jsonify({"error": GENERAL_SERVER_ERROR}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task", methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "name field is not provided"}), HTTPStatus.BAD_REQUEST
        return jsonify({"result": task_records.add()}), HTTPStatus.CREATED
    except Exception as ex:
        logger.exception("Exception when adding task: %r", ex)
        return jsonify({"error": GENERAL_SERVER_ERROR}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task/<int:t_id>", methods=['PUT'])
def update_task(t_id: int):
    try:
        data = request.get_json()
        return jsonify({"result": task_records.update(t_id, data)})
    except KeyError:
        return jsonify({"error": "id does not exist"}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        logger.exception("Exception when updating task: %r", ex)
        return jsonify({"error": GENERAL_SERVER_ERROR}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/task/<int:t_id>", methods=['DELETE'])
def delete_task(t_id: int):
    try:
        task_records.delete(t_id)
        return '', HTTPStatus.OK
    except KeyError:
        return jsonify({"error": "id does not exist"}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        logger.exception("Exception when updating task: %r", ex)
        return jsonify({"error": GENERAL_SERVER_ERROR}), HTTPStatus.INTERNAL_SERVER_ERROR
