from flask import jsonify

from main.app import app
from main.consts import AccountType
from main.libs.validate import validate_data
from main.libs.auth_require import auth_require
from main.schemas.item import ItemSchema, UpdateItemSchema
from main.models.item import ItemModel
from main.models.category import CategoryModel
from main.errors import PermissionDenied, ItemNotFound, CategoryNotFound


@app.route('/items', methods=['POST'])
@auth_require(AccountType.USER)
@validate_data(ItemSchema())
def create_item(data, user):
    category = CategoryModel.query.get(data['category_id'])
    if category is None:
        raise CategoryNotFound()

    new_item = ItemModel(
        title=data['title'],
        content=data['content'],
        category_id=data['category_id'],
        user_id=user.id,
    )
    new_item.save_to_db()

    return jsonify({'data': None}), 201


@app.route('/items', methods=['GET'])
@auth_require(AccountType.USER)
def get_items(user):
    items = ItemModel.query.all()

    return jsonify({'data': [item.json() for item in items]})


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@auth_require(AccountType.USER)
def get_category_items(user, category_id):
    items = ItemModel.query.filter_by(category_id=category_id)

    return jsonify({'data': [item.json() for item in items]})


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@auth_require(AccountType.USER)
@validate_data(UpdateItemSchema())
def update_category_item(user, data, category_id, item_id):
    item = ItemModel.query.filter_by(id=item_id, category_id=category_id).first()

    if not item:
        raise ItemNotFound()

    if item.user_id != user.id:
        raise PermissionDenied()

    item.title = data['title']
    item.content = data['content']

    item.save_to_db()

    return jsonify({'data': None})


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@auth_require(AccountType.USER)
def delete_item(user, category_id, item_id):
    item = ItemModel.query.filter_by(id=item_id, category_id=category_id).first()

    if not item:
        raise ItemNotFound()

    if item.user_id != user.id:
        raise PermissionDenied()

    item.delete_from_db()

    return jsonify({'data': None})
