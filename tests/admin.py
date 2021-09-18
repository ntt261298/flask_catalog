from flask import json

from config import app_config


class TestAdmin:
    config = app_config["test"]

    def get_admin_authentication_headers(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin/login",
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

    # To make db test works in this module
    def test_db(self, db_test):
        assert db_test

    def test_create_valid_admin(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin",
            data=json.dumps(
                {"username": "valid_username", "password": "random_password"}
            ),
            headers=self.get_admin_authentication_headers(testing_client, test_admin),
        )
        json_response = json.loads(response.data)
        assert response.status_code == 201
        assert json_response == {"data": None}

    def test_create_invalid_username_password(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin",
            data=json.dumps({"username": "", "password": "123"}),
            headers=self.get_admin_authentication_headers(testing_client, test_admin),
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

    def test_create_duplicated_username(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin",
            data=json.dumps(
                {"username": test_admin["username"], "password": "123456"}
            ),
            headers=self.get_admin_authentication_headers(testing_client, test_admin),
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

    def test_unauthorized_create(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin",
            data=json.dumps(
                {"username": test_admin["username"], "password": "123456"}
            ),
            headers={"Content-Type": "application/json", "Authentication": "Bearer fake_token"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 401
        assert json_response == {
            "error": {
                "error_message": "Unauthorized",
                "error_code": 401000,
                "error_data": None,
            }
        }

    def test_login_valid_admin(self, testing_client, test_admin):
        response = testing_client.post(
            self.config.API_URL + "/admin/login",
            data=json.dumps(
                {
                    "username": test_admin["username"],
                    "password": test_admin["password"],
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

    def test_login_invalid_username_password(self, testing_client):
        response = testing_client.post(
            self.config.API_URL + "/admin/login",
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

    def test_login_invalid_admin(self, testing_client):
        response = testing_client.post(
            self.config.API_URL + "/admin/login",
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
