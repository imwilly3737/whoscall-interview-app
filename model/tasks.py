from os import getenv

import redis

_r = redis.Redis(host="redis", port=6379, decode_responses=True)
if getenv("TEST") is None:
    AUTO_INCREMENT = "AUTO_INCREMENT"
    SET_KEY = "TASKS_SET"
    TASK_PREFIX = "TASKS:"
else:
    AUTO_INCREMENT = "TEST_AUTO_INCREMENT"
    SET_KEY = "TEST_TASKS_SET"
    TASK_PREFIX = "TEST_TASKS:"


class Tasks:

    VALID_FIELDS = ["id", "name", "status"]

    class Status:
        INCOMPLETE = 0
        COMPLETE = 1

    def __init__(self):
        if _r.get(AUTO_INCREMENT) is None:
            _r.set(AUTO_INCREMENT, 1)

    @staticmethod
    def get_auto_increment():
        return int(_r.get(AUTO_INCREMENT))

    @staticmethod
    def increase_auto_increment():
        _r.incr(AUTO_INCREMENT)

    @staticmethod
    def storage_get_all() -> list:
        tid_set = _r.smembers(SET_KEY)
        storage_result = []
        for tid in tid_set:
            storage_result.append(Tasks.storage_get(tid))
        return storage_result

    @staticmethod
    def storage_get(tid) -> dict:
        t_dict = _r.hgetall(TASK_PREFIX + str(tid))
        t_dict["id"] = int(t_dict["id"])
        t_dict["status"] = int(t_dict["status"])
        return t_dict

    @staticmethod
    def storage_add(tid, record):
        _r.sadd(SET_KEY, tid)
        _r.hset(TASK_PREFIX + str(tid), mapping=record)

    @staticmethod
    def storage_update(tid, record):
        _r.hset(TASK_PREFIX + str(tid), mapping=record)

    @staticmethod
    def storage_delete(tid):
        _r.srem(SET_KEY, tid)
        _r.delete(TASK_PREFIX + str(tid))

    def query(self) -> list:
        return self.storage_get_all()

    def add(self, name: str) -> dict:
        record = {
            "id": int(self.get_auto_increment()),
            "name": name,
            "status": self.Status.INCOMPLETE
        }
        self.storage_add(self.get_auto_increment(), record)
        self.increase_auto_increment()
        return record

    def update(self, t_id: int, fields: dict) -> dict:
        fields = {k: v for k, v in fields.items() if k in self.VALID_FIELDS}
        if t_id != fields.get('id', t_id):
            raise KeyError
        if not _r.sismember(SET_KEY, str(t_id)):
            raise KeyError
        self.storage_update(t_id, fields)
        return self.storage_get(t_id)

    def delete(self, t_id: int):
        if not _r.sismember(SET_KEY, str(t_id)):
            raise KeyError
        self.storage_delete(t_id)

    @staticmethod
    def clear_all():
        _r.flushall()


task_records = Tasks()
