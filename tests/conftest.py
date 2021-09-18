import pytest
import bcrypt

from app import db, app
from models.user import UserModel
from models.admin import AdminModel


@pytest.fixture(scope='module')
def db_test():
    db.session.remove()
    db.drop_all()
    db.create_all()
    return db


@pytest.fixture(scope='module')
def testing_client():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


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
