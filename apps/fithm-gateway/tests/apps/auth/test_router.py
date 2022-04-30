def test_app_starts(app):
    print(type(app))


# def test_auth_sign_up(app):
#     response = app.test_client().post('api/v1/auth/signup',
#                                       json={"email": "test@test.com", "password": "password", "username": "test"}
#                                       )
#     print(response.json)


# def test_auth_sign_in(app):
#     response = app.test_client().post('api/v1/auth/signin',
#                                       json={"email": "test@test.com", "password": "password"}
#                                       )
#     assert response.status_code == 200


def test_get_accounts(app, token):
    with app.test_request_context():
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
