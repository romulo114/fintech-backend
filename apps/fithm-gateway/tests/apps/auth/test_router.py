import requests
import requests_mock


def test_app_starts(app):
    pass


def test_auth_sign_in(app):
    response = app.test_client().post('api/v1/auth/signin',
                                      json={"email": "test@test.com", "password": "password"}
                                      )
    assert response.status_code == 200


def test_get_accounts(app, token):
    with app.test_request_context():
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST', 'http://tradeshop:5050/api/v1/accounts', json={})
            response = app.test_client().post(
                "api/v1/accounts",
                headers={"Authorization": f"Bearer {token['tokens']['access_token']}"},
                json={
                    "email": "test@test.com",
                    "password": "password",
                    "broker_name": "test broker",
                    "account_number": "test account",
                },
            )
    assert response.status_code == 200
