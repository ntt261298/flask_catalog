from functools import wraps

import jwt
from flask import request

from main.app import app
from main.consts import AccountType
from main.errors import UnauthorizedRequest
from main.models.user import UserModel
from main.models.admin import AdminModel


def auth_require(account_type=None):
    def authentication(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            authorization = request.headers.get('Authorization')

            if authorization is None:
                raise UnauthorizedRequest()
            access_token = authorization.replace("Bearer ", "")
            if not access_token:
                raise UnauthorizedRequest()

            try:
                decoded = jwt.decode(access_token, app.config['JWT_SECRET'], algorithms="HS256")
            except:
                decoded = None

            if not decoded:
                raise UnauthorizedRequest()

            account_id = decoded.get('id')

            if account_type == AccountType.USER:
                account = UserModel.query.get(account_id)
            elif account_type == AccountType.ADMIN:
                account = AdminModel.query.get(account_id)
            else:
                raise Exception('Invalid account type')

            if not account:
                raise UnauthorizedRequest()

            kwargs[account_type] = account

            return f(*args, **kwargs)
        return decorator_function
    return authentication
