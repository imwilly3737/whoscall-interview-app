from http import HTTPStatus
import logging
from os import getenv
import time

import requests

from model.tasks import Tasks
from unit_tests.model.test_tasks import check_query_result

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

URL = "http://localhost:5000"
LOGIN_URL = URL + "/login"
TASKS_URL = URL + "/tasks"
TASK_URL = URL + "/task"


def get_jwt_token() -> str:
    response = requests.post(LOGIN_URL, json={
        "username": getenv('USER_NAME', 'whoscall'),
        "password": getenv('USER_PASSWORD', 'wrong-password')
    })
    data = response.json()
    return data["access_token"]


def e2e_test_auth_and_crud():
    # Check Unauthorized result
    response = requests.get(TASKS_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    jwt_token = get_jwt_token()
    logger.info('Check Unauthorized result: Success')

    # Check Authorized result
    response = requests.get(TASKS_URL, headers={
        "Authorization": f"Bearer {jwt_token}",
    })
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert result == {'result': []}
    logger.info('Check Authorized result: Success')

    # Check Task creation
    response = requests.post(TASK_URL, headers={
        "Authorization": f"Bearer {jwt_token}",
    }, json={
        "name": "買晚餐",
    })
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    tid = response_json["result"]["id"]
    assert response.json() == {"result": {
        "id": tid,
        "name": "買晚餐",
        "status": Tasks.Status.INCOMPLETE,
    }}
    logger.info('Check Task creation: Success')

    # Check Task read
    response = requests.get(TASKS_URL, headers={
        "Authorization": f"Bearer {jwt_token}",
    })
    assert response.status_code == HTTPStatus.OK
    result = response.json()["result"]
    check_query_result(result, {
        tid: {
            "id": tid,
            "name": "買晚餐",
            "status": Tasks.Status.INCOMPLETE,
        }
    })
    logger.info('Check Task read: Success')

    # Check Task update
    response = requests.put(TASK_URL + f"/{tid}", headers={
        "Authorization": f"Bearer {jwt_token}",
    }, json={
        "status": Tasks.Status.COMPLETE,
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"result": {
        "id": tid,
        "name": "買晚餐",
        "status": Tasks.Status.COMPLETE
    }}
    logger.info('Check Task Update: Success')

    # Check Task deletion
    response = requests.delete(TASK_URL + f"/{tid}", headers={
        "Authorization": f"Bearer {jwt_token}",
    })
    assert response.status_code == HTTPStatus.OK
    logger.info('Check Task deletion: Success')

    # Check Authorization expired
    logger.info('Sleep 60 seconds to check the result of authorization expiration')
    time.sleep(60)
    response = requests.get(TASKS_URL, headers={
        "Authorization": f"Bearer {jwt_token}",
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    logger.info('Check Authorization expired: Success')

    logger.info('Success!! All Checks are completed without problems.')

    Tasks.clear_all()


if __name__ == "__main__":
    if getenv("TEST") is None:
        raise Exception("Do not run this on NON-TESTING mode")
    e2e_test_auth_and_crud()
