import pytest

from app import db, app


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
