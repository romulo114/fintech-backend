
def test_app_starts(app):
    print(type(app))

def test_auth_sign_in(app):
    response = app.post('api/v1/auth/signin', json={"email": "info@fithm.com", "password": "Horse@20180902"})
    print(response, type(response))
    # assert response.status_code == 200
