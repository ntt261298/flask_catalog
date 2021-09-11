from flask import jsonify
from marshmallow import Schema, fields

from app import app


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INTERNAL_SERVER = 500


class ErrorCode:
    BAD_REQUEST = 400000
    UNAUTHORIZED = 401000
    INTERNAL_SERVER = 50000


class ErrorSchema(Schema):
    error_code = fields.Int()
    error_message = fields.String()
    error_data = fields.Raw()


class Error(Exception):
    def __init__(self, error_data=None):
        super().__init__()
        self.error_data = error_data

    def to_response(self):
        return jsonify({
            "error": ErrorSchema().dump(self)
        })


class BadRequest(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.BAD_REQUEST
    error_message = "Bad request"


class RegisteredAccount(BadRequest):
    error_message = "This username is already registered."


class InvalidAccount(BadRequest):
    error_message = "Invalid username or password."


class UnauthorizedRequest(Error):
    status_code = StatusCode.UNAUTHORIZED
    error_code = ErrorCode.UNAUTHORIZED
    error_message = "Unauthorized"


@app.errorhandler(Error)
def handle_exception(error):
    return error.to_response(), error.status_code
