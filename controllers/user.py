import bcrypt
import jwt
from flask import jsonify

from app import app
from errors import RegisteredAccount, InvalidAccount
from libs.validate import validate_data
from models.user import UserModel
from schemas.user import UserSchema


@app.route('/user/register', methods=['POST'])
@validate_data(UserSchema())
def register_user(data):
    user = UserModel.query.filter_by(username=data['username']).first()

    if user:
        raise RegisteredAccount()

    hashed = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())

    new_user = UserModel(username=data['username'], password=hashed)
    new_user.save_to_db()

    return jsonify({'data': None}), 201


@app.route('/user/login', methods=['POST'])
@validate_data(UserSchema())
def login_user(data):
    user = UserModel.query.filter_by(username=data['username']).first()

    if not user:
        raise InvalidAccount()

    if not bcrypt.checkpw(data['password'].encode('utf8'), user.password.encode('utf8')):
        raise InvalidAccount()

    access_token = jwt.encode({
        'id': user.id,
    }, app.config['JWT_SECRET'])

    return jsonify({'data': {'access_token': access_token}}), 200
