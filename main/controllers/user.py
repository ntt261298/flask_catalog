from flask import jsonify

from main.app import app
from main.consts import AccountType
from main.libs.validate import validate_data
from main.schemas.account import AccountSchema
from main.engines.account import create_new_account, get_account_token


@app.route('/user/register', methods=['POST'])
@validate_data(AccountSchema())
def register_user(data):
    create_new_account(
        account_type=AccountType.USER,
        data=data
    )
    return jsonify({'data': None}), 201


@app.route('/user/login', methods=['POST'])
@validate_data(AccountSchema())
def login_user(data):
    access_token = get_account_token(
        account_type=AccountType.USER,
        data=data
    )
    return jsonify({'data': {'access_token': access_token}}), 200
