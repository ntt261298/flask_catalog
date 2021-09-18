import jwt
import bcrypt

from main.app import app
from main.consts import AccountType
from main.models.user import UserModel
from main.models.admin import AdminModel
from main.errors import RegisteredAccount, InvalidAccount


def get_account_model(account_type):
    if account_type == AccountType.ADMIN:
        return AdminModel
    elif account_type == AccountType.USER:
        return UserModel
    else:
        raise Exception('Invalid account type')


def create_new_account(account_type, data):
    account_model = get_account_model(account_type)
    account = account_model.query.filter_by(username=data['username']).first()

    if account:
        raise RegisteredAccount()

    hashed = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())

    new_account = account_model(username=data['username'], password=hashed)
    new_account.save_to_db()


def get_account_token(account_type, data):
    account_model = get_account_model(account_type)
    account = account_model.query.filter_by(username=data['username']).first()

    if not account:
        raise InvalidAccount()

    if not bcrypt.checkpw(data['password'].encode('utf8'), account.password.encode('utf8')):
        raise InvalidAccount()

    return jwt.encode({
        'id': account.id,
    }, app.config['JWT_SECRET'])
