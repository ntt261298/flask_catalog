from flask import jsonify

from app import app
from consts import AccountType
from libs.validate import validate_data
from libs.auth_require import auth_require
from schemas.category import CategorySchema
from models.category import CategoryModel
from errors import ExistedCategory


@app.route('/categories', methods=['POST'])
@auth_require(AccountType.ADMIN)
@validate_data(CategorySchema())
def create_category(data, admin):
    category = CategoryModel.query.filter_by(name=data['name']).first()

    if category:
        raise ExistedCategory()

    new_category = CategoryModel(name=data['name'])
    new_category.save_to_db()

    return jsonify({'data': None}), 201


@app.route('/categories', methods=['GET'])
@auth_require(AccountType.USER)
def get_categories(user):
    categories = CategoryModel.query.all()

    return jsonify({'data': [category.json() for category in categories]})
