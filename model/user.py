from os import getenv


class User:

    def __init__(self):
        self._storage = {
            "whoscall": {
                "username": "whoscall",
                "password": getenv("USER_PASSWORD"),
            }
        }

    def query_user(self, username, password) -> bool:
        if username in self._storage and self._storage[username]["password"] == password:
            return True
        return False


user_records = User()
