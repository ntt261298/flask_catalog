from flask import json


class TestUser:
    # To make db test works in this module
    def test_db(self, db_test):
        assert db_test

    def test_register_valid_user(self, config, testing_client):
        response = testing_client.post(
            config.API_URL + "/user/register",
            data=json.dumps(
                {"username": "valid_username", "password": "random_password"}
            ),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 201
        assert json_response == {'data': None}

    def test_register_invalid_username_password(self, config, testing_client):
        response = testing_client.post(
            config.API_URL + "/user/register",
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

    def test_register_duplicated_username(self, config, testing_client, test_user):
        response = testing_client.post(
            config.API_URL + "/user/register",
            data=json.dumps(
                {"username": test_user["username"], "password": "123456"}
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

    def test_login_valid_user(self, config, testing_client, test_user):
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
        assert response.status_code == 200
        assert json_response == {
            "data": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.Ug2NvAlOyhVvu53NLUc2rXG1C9mTNLGbZVId_eoSO48"
            }
        }

    def test_login_invalid_username_password(self, config, testing_client):
        response = testing_client.post(
            config.API_URL + "/user/login",
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

    def test_login_invalid_user(self, config, testing_client):
        response = testing_client.post(
            config.API_URL + "/user/login",
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
