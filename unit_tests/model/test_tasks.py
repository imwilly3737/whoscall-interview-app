import pytest

from model.tasks import Tasks


def check_query_result(result, expect_result):
    assert len(expect_result) == len(result)
    for _r in result:
        assert expect_result[_r["id"]] == _r


@pytest.fixture()
def prepare_empty_task():
    return Tasks()


@pytest.fixture()
def prepare_one_task():
    _tasks = Tasks()
    _tasks._storage = {
        1: {
            "id": 1,
            "name": "task1",
            "status": Tasks.Status.INCOMPLETE
        }
    }
    _tasks._auto_increment = 2
    return _tasks


def test_empty_query(prepare_empty_task):
    _tasks = prepare_empty_task
    assert _tasks.query() == []


@pytest.mark.parametrize("new_task_name,add_expected,query_expected", [
    ("new_name",
     {"id": 1, "name": "new_name", "status": Tasks.Status.INCOMPLETE},
     {1: {"id": 1, "name": "new_name", "status": Tasks.Status.INCOMPLETE}}
     ),
    ("新名字",
     {"id": 1, "name": "新名字", "status": Tasks.Status.INCOMPLETE},
     {1: {"id": 1, "name": "新名字", "status": Tasks.Status.INCOMPLETE}}
     ),
])
def test_add_task(prepare_empty_task, new_task_name, add_expected, query_expected):
    _tasks = prepare_empty_task
    assert add_expected == _tasks.add(new_task_name)
    query_result = _tasks.query()
    check_query_result(query_result, query_expected)


@pytest.mark.parametrize("tid,new_payload,update_expected,query_expected", [
    (1, {"name": "updated_name"},
     {"id": 1, "name": "updated_name", "status": Tasks.Status.INCOMPLETE},
     {1: {"id": 1, "name": "updated_name", "status": Tasks.Status.INCOMPLETE}}
     ),
    (1, {"status": Tasks.Status.COMPLETE},
     {"id": 1, "name": "task1", "status": Tasks.Status.COMPLETE},
     {1: {"id": 1, "name": "task1", "status": Tasks.Status.COMPLETE}}
     ),
])
def test_update_task(prepare_one_task, tid, new_payload, update_expected, query_expected):
    _tasks = prepare_one_task
    assert update_expected == _tasks.update(tid, new_payload)
    query_result = _tasks.query()
    check_query_result(query_result, query_expected)


@pytest.mark.parametrize("tid,key_error,query_expected", [
    (1, False, {}),
    (100, True, {1: {"id": 1, "name": "task1", "status": Tasks.Status.INCOMPLETE}})
])
def test_delete_task(prepare_one_task, tid, key_error, query_expected):
    _tasks = prepare_one_task
    if key_error:
        with pytest.raises(KeyError):
            _tasks.delete(tid)
    else:
        _tasks.delete(tid)
    query_result = _tasks.query()
    check_query_result(query_result, query_expected)
