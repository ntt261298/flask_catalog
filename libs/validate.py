from functools import wraps

from flask import request
from marshmallow import ValidationError

from errors import BadRequest


def validate_data(schema):
    def parse_data(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            request_json = request.get_json()

            try:
                request_data = schema.load(request_json)
            except ValidationError as err:
                raise BadRequest(error_data=err.messages)
            return f(data=request_data, *args, **kwargs)
        return decorator_function
    return parse_data


def validate_args(schema):
    def parse_args(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            request_args = request.args

            try:
                request_data = schema.load(request_args)
            except ValidationError as err:
                raise BadRequest(error_data=err)
            return f(data=request_data, *args, **kwargs)
        return decorator_function
    return parse_args
