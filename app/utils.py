from functools import wraps
from http import HTTPStatus


def json_response(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        r = f(*args, **kwargs)
        if isinstance(r, tuple):
            return *r, {"Content-Type": 'application/json; charset=utf-8'}
        return r, HTTPStatus.OK, {"Content-Type": 'application/json; charset=utf-8'}
    return inner_func
