from os import getenv

import redis

AUTO_INCREMENT = "AUTO_INCREMENT"
SET_KEY = "TASKS_SET"
TASK_PREFIX = "TASKS:"


class Tasks:
    if getenv("UNIT_TEST") is None:
        _r = redis.Redis(host="redis", port=6379)
    else:
        _r = None
    VALID_FIELDS = ["id", "name", "status"]

    class Status:
        INCOMPLETE = 0
        COMPLETE = 1

    def __init__(self):
        self._storage = {}
        if self._r and self._r.get(AUTO_INCREMENT) is None:
            self._r.set(AUTO_INCREMENT, 1)

    def get_auto_increment(self):
        return int(self._r.get(AUTO_INCREMENT))

    def increase_auto_increment(self):
        self._r.incr(AUTO_INCREMENT)

    def query(self) -> list:
        return list(self._storage.values())

    def add(self, name: str) -> dict:
        record = {
            "id": self.get_auto_increment(),
            "name": name,
            "status": self.Status.INCOMPLETE
        }
        self._storage[self.get_auto_increment()] = record
        self.increase_auto_increment()
        return record

    def update(self, t_id: int, fields: dict) -> dict:
        fields = {k: v for k, v in fields.items() if k in self.VALID_FIELDS}
        self._storage[t_id].update(fields)
        return self._storage[t_id]

    def delete(self, t_id: int):
        del self._storage[t_id]


task_records = Tasks()
