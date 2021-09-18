from flask import json


class TestCategory:
    # To make db test works in this module
    def test_db(self, db_test):
        assert db_test

    def test_create_valid_category(
        self, config, testing_client, admin_authentication_headers
    ):
        response = testing_client.post(
            config.API_URL + "/categories",
            data=json.dumps({"name": "New Category"}),
            headers=admin_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 201
        assert json_response == {"data": None}

    def test_create_empty_name(
        self, config, testing_client, admin_authentication_headers
    ):
        response = testing_client.post(
            config.API_URL + "/categories",
            data=json.dumps({"name": ""}),
            headers=admin_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": {"name": ["Shorter than minimum length 1."]},
                "error_message": "Bad request",
            }
        }

    def test_create_duplicated_name(
        self, config, testing_client, admin_authentication_headers, test_category
    ):
        response = testing_client.post(
            config.API_URL + "/categories",
            data=json.dumps({"name": test_category["name"]}),
            headers=admin_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": None,
                "error_message": "This category is already existed",
            }
        }

    def test_unauthorized_create(
        self,
        config,
        testing_client,
    ):
        response = testing_client.post(
            config.API_URL + "/categories",
            data=json.dumps({"name": "random name"}),
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 401
        assert json_response == {
            "error": {
                "error_code": 401000,
                "error_data": None,
                "error_message": "Unauthorized",
            }
        }

    def test_get_all_categories(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.get(
            config.API_URL + "/categories",
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {
            "data": [{"id": 1, "name": "New Category"}, {"id": 2, "name": "Category"}]
        }

    def test_unauthorized_get(self, config, testing_client):
        response = testing_client.get(
            config.API_URL + "/categories",
            headers={"Content-Type": "application/json"},
        )
        json_response = json.loads(response.data)
        assert response.status_code == 401
        assert json_response == {
            "error": {
                "error_code": 401000,
                "error_data": None,
                "error_message": "Unauthorized",
            }
        }
