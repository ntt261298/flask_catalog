from functools import wraps

import jwt
from flask import request

from app import app
from consts import AccountType
from errors import UnauthorizedRequest
from models.user import UserModel
from models.admin import AdminModel


def auth_require(account_type):
    def authentication(f):
        wraps(f)
        def decorator_function(*args, **kwargs):
            if account_type == AccountType.USER:
                account_model = UserModel
            elif account_type == AccountType.ADMIN:
                account_model = AdminModel
            else:
                raise Exception('Invalid account type')

            authorization = request.headers.get('Authorization')

            if authorization is None:
                raise UnauthorizedRequest()
            access_token = authorization.replace("Bearer ", "")
            if not access_token:
                raise UnauthorizedRequest()

            decoded = jwt.decode(access_token, app.config['JWT_SECRET'], algorithms="HS256")

            if not decoded:
                return UnauthorizedRequest()

            account_id = decoded.get('id')
            account = account_model.query.get(account_id)

            if not account:
                raise UnauthorizedRequest()

            kwargs[account_type] = account
            return f(*args, **kwargs)
        return decorator_function
    return authentication
