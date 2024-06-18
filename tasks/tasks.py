class Tasks:
    _storage = {}
    _auto_increment = 1
    VALID_FIELDS = ["id", "name", "status"]

    class Status:
        INCOMPLETE = 0
        COMPLETE = 1

    def query(self) -> list:
        return list(self._storage.values())

    def add(self, name: str) -> dict:
        record = {
            "id": self._auto_increment,
            "name": name,
            "status": self.Status.INCOMPLETE
        }
        self._storage[self._auto_increment] = record
        self._auto_increment += 1
        return record

    def update(self, t_id: int, fields: dict) -> dict:
        fields = {k: v for k, v in fields.items() if k in self.VALID_FIELDS}
        self._storage[t_id].update(fields)
        return self._storage[t_id]

    def delete(self, t_id: int):
        del self._storage[t_id]


task_records = Tasks()
