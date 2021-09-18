from flask import json


class TestItem:
    # To make db test works in this module
    def test_db(self, db_test):
        assert db_test

    # To create test category for this module, which has id: 1
    def test_category(self, test_category):
        assert test_category

    def test_create_valid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.post(
            config.API_URL + "/items",
            data=json.dumps(
                {
                    "title": "Item title",
                    "content": "Item content",
                    "category_id": 1,
                }
            ),
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 201
        assert json_response == {"data": None}

    def test_create_invalid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.post(
            config.API_URL + "/items",
            data=json.dumps(
                {
                    "title": "",
                    "content": "",
                }
            ),
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": {
                    "category_id": ["Missing data for required field."],
                    "content": ["Shorter than minimum length 1."],
                    "title": ["Shorter than minimum length 1."],
                },
                "error_message": "Bad request",
            }
        }

    def test_create_invalid_category_id(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.post(
            config.API_URL + "/items",
            data=json.dumps(
                {
                    "title": "Item title",
                    "content": "Item content",
                    "category_id": 2,  # This category isn't existed
                }
            ),
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": None,
                "error_message": "Can not find the category",
            }
        }

    def test_unauthorized_create(self, config, testing_client):
        response = testing_client.post(
            config.API_URL + "/items",
            data=json.dumps(
                {
                    "title": "Item title",
                    "content": "Item content",
                    "category_id": 1,
                }
            ),
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

    def test_get_all_items(self, config, testing_client, user_authentication_headers):
        response = testing_client.get(
            config.API_URL + "/items",
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {
            "data": [{"content": "Item content", "id": 1, "title": "Item title"}]
        }

    def test_unauthorized_get_all(self, config, testing_client):
        response = testing_client.get(
            config.API_URL + "/items",
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

    def test_get_all_category_items(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.get(
            config.API_URL + "/categories/1/items",
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {
            "data": [{"content": "Item content", "id": 1, "title": "Item title"}]
        }

    def test_unauthorized_get_all_category_items(self, config, testing_client):
        response = testing_client.get(
            config.API_URL + "/categories/1/items",
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

    def test_update_valid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.put(
            config.API_URL + "/categories/1/items/1",
            data=json.dumps(
                {
                    "title": "Updated item title",
                    "content": "Updated item content",
                }
            ),
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {"data": None}

    def test_update_invalid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.put(
            config.API_URL + "/categories/1/items/1",
            data=json.dumps(
                {
                    "title": "",
                    "content": "Updated item content",
                }
            ),
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": {"title": ["Shorter than minimum length 1."]},
                "error_message": "Bad request",
            }
        }

    def test_unauthorized_update(self, config, testing_client):
        response = testing_client.put(
            config.API_URL + "/categories/1/items/1",
            data=json.dumps(
                {
                    "title": "Updated item title",
                    "content": "Updated item content",
                }
            ),
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

    def test_delete_valid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.delete(
            config.API_URL + "/categories/1/items/1",
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 200
        assert json_response == {"data": None}

    def test_delete_invalid_item(
        self, config, testing_client, user_authentication_headers
    ):
        response = testing_client.delete(
            config.API_URL + "/categories/10/items/1",  # Category 10 isn't existed
            headers=user_authentication_headers,
        )
        json_response = json.loads(response.data)
        assert response.status_code == 400
        assert json_response == {
            "error": {
                "error_code": 400000,
                "error_data": None,
                "error_message": "Can not find the item",
            }
        }

    def test_unauthorized_delete(self, config, testing_client):
        response = testing_client.delete(
            config.API_URL + "/categories/1/items/1",
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
