import pytest
import bcrypt
from flask import json

from main.app import db, app
from config import app_config
from main.models.user import UserModel
from main.models.admin import AdminModel
from main.models.category import CategoryModel


@pytest.fixture(scope='module')
def config():
    return app_config["test"]


@pytest.fixture(scope='module')
def db_test():
    db.session.remove()
    db.drop_all()
    db.create_all()
    return db


@pytest.fixture(scope='module')
def testing_client():
    # Create a test client using the Flask application configured for testing
    return app.test_client()


@pytest.fixture(scope='module')
def test_user(db_test):
    test_user = {
        "username": "truong_nguyen",
        "password": "123456"
    }
    user = UserModel(
        username=test_user["username"],
        password=bcrypt.hashpw(
            test_user["password"].encode("utf8"), bcrypt.gensalt()
        ),
    )
    user.save_to_db()
    return test_user


@pytest.fixture(scope='module')
def user_authentication_headers(config, testing_client, test_user):
    response = testing_client.post(
        config.API_URL + "/user/login",
        data=json.dumps(
            {
                "username": test_user["username"],
                "password": test_user["password"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    json_response = json.loads(response.data)
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + json_response["data"]["access_token"],
    }


@pytest.fixture(scope='module')
def test_admin(db_test):
    test_admin = {
        "username": "truong_admin",
        "password": "123456"
    }
    admin = AdminModel(
        username=test_admin["username"],
        password=bcrypt.hashpw(
            test_admin["password"].encode("utf8"), bcrypt.gensalt()
        ),
    )
    admin.save_to_db()
    return test_admin


@pytest.fixture(scope='module')
def admin_authentication_headers(config, testing_client, test_admin):
    response = testing_client.post(
        config.API_URL + "/admin/login",
        data=json.dumps(
            {
                "username": test_admin["username"],
                "password": test_admin["password"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    json_response = json.loads(response.data)
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + json_response["data"]["access_token"],
    }


@pytest.fixture(scope='module')
def test_category(db_test):
    test_category = {
        "name": "Category",
    }
    category = CategoryModel(
        name=test_category["name"],
    )
    category.save_to_db()
    return test_category
