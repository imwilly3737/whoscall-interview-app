from os import getenv


class User:
    _storage = {
        "whoscall": {
            "username": "whoscall",
            "password": getenv("USER_PASSWORD"),
        }
    }

    @classmethod
    def query_user(cls, username, password) -> bool:
        if username in cls._storage and cls._storage[username]["password"] == password:
            return True
        return False
