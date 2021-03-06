from flask import jsonify

from main.app import app
from main.consts import AccountType
from main.libs.validate import validate_data
from main.libs.auth_require import auth_require
from main.schemas.account import AccountSchema
from main.engines.account import create_new_account, get_account_token


@app.route('/admin', methods=['POST'])
@validate_data(AccountSchema())
@auth_require(AccountType.ADMIN)
def create_admin(admin, data):
    create_new_account(
        account_type=AccountType.ADMIN,
        data=data
    )
    return jsonify({'data': None}), 201


@app.route('/admin/login', methods=['POST'])
@validate_data(AccountSchema())
def login_admin(data):
    access_token = get_account_token(
        account_type=AccountType.ADMIN,
        data=data
    )
    return jsonify({'data': {'access_token': access_token}}), 200
