from flask import jsonify

from app import app
from libs.validate import validate_data
from libs.auth_require import auth_require
from schemas.category import CategorySchema
from models.category import CategoryModel
from errors import ExistedCategory


@app.route('/categories', methods=['POST'])
@auth_require('admin')
@validate_data(CategorySchema())
def create_category(data, admin):
    category = CategoryModel.query.filter_by(name=data['name'])

    if category:
        raise ExistedCategory()

    new_category = CategoryModel(name=data['name'])
    new_category.save_to_db()

    return jsonify({'data': None})


@app.route('/categories', methods=['GET'])
@auth_require('user')
def get_categories(user):
    categories = CategoryModel.query.all()

    return jsonify({'data': [category.json() for category in categories]})
