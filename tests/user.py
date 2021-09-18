import bcrypt
from flask import json

from config import app_config
from models.user import UserModel


class TestUser:
    test_account = {
        'username': 'truong_nguyen',
        'password': '123456',
    }

    config = app_config['test']

    def create_test_user(self):
        user = UserModel(
            username=self.test_account["username"],
            password=bcrypt.hashpw(
                self.test_account["password"].encode("utf8"), bcrypt.gensalt()
            ),
        )
        user.save_to_db()

    def test_register_valid_user(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/register",
            data=json.dumps(
                {"username": "valid_username", "password": "random_password"}
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 201
        assert json_response == {'data': None}

    def test_register_invalid_username_password(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/register",
            data=json.dumps({"username": "", "password": "123"}),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_message": "Bad request",
                "error_code": 400000,
                "error_data": {
                    "username": ["Shorter than minimum length 1."],
                    "password": ["Shorter than minimum length 6."],
                },
            }
        }

    def test_register_duplicated_username(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/register",
            data=json.dumps(
                {"username": self.test_account["username"], "password": "123456"}
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_message": "This username is already registered",
                "error_code": 400000,
                "error_data": None,
            }
        }

    def test_login_valid_user(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/login",
            data=json.dumps(
                {
                    "username": self.test_account["username"],
                    "password": self.test_account["password"],
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {
            "data": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.QqM2waRIwGDr5FIsF96HmugLxLUwu5ZGjyExxG9DpL0"
            }
        }

    def test_login_invalid_username_password(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/login",
            data=json.dumps(
                {
                    "username": "",
                    "password": "123",
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": {
                    "password": ["Shorter than minimum length 6."],
                    "username": ["Shorter than minimum length 1."],
                },
                "error_message": "Bad request",
            }
        }

    def test_login_invalid_user(self, testing_client, db_test):
        self.create_test_user()
        response = testing_client.post(
            self.config.API_URL + "/user/login",
            data=json.dumps(
                {
                    "username": "truong_nguyen",
                    "password": "fake_password",
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": None,
                "error_message": "Invalid username or password",
            }
        }
