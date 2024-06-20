from http import HTTPStatus
from os import getenv

import requests

URL = "http://localhost:5000"
LOGIN_URL = URL + "/login"
TASKS_URL = URL + "/tasks"
TASK_URL = URL + "/task"


def get_jwt_token() -> str:
    response = requests.post(URL + "/login", json={
        "username": getenv('USER_NAME', 'whoscall'),
        "password": getenv('USER_PASSWORD', 'wrong-password')
    })
    data = response.json()
    return data["access_token"]


def e2e_test_auth_and_crud():
    response = requests.get(URL + "/tasks")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    jwt_token = get_jwt_token()

    response = requests.get(URL + "/tasks", headers={
        'Authorization': f"Bearer {jwt_token}",
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'result': []}


if __name__ == "__main__":
    e2e_test_auth_and_crud()
