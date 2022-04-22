
def test_app_starts(app):
    print(type(app))


def test_create_object_from_db(create_user):
    print(create_user)


def test_auth_sign_in(app):
    response = app.test_client().post('api/v1/auth/signin',
                                      json={"email": "info@fithm.com", "password": "Horse@20180902"}
                                      )
    assert response.status_code == 200


def test_get_accounts(app, token, postgresql):
    response = app.test_client().post('api/v1/accounts', headers={},
                                      json={"email": "info@fithm.com", "password": "Horse@20180902"}
                                      )
    assert response.status_code == 200