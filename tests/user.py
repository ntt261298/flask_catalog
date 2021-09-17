from flask import json

from config import app_config


class TestUser:
    test_account = {
        'username': 'truong_nguyen',
        'password': '123456',
    }

    config = app_config['test']

    def test_auth_invalid_user_password(self, testing_client, db_test):
        response = testing_client.post(
            self.config.API_URL + '/user/register',
            data=json.dumps({
                'username': self.test_account['username'],
                'password': 'random_password'
            }),
            headers={
                'Content-Type': 'application/json'
            }
        )
        json_response = json.loads(response.data)
        assert json_response == {'data': None}
