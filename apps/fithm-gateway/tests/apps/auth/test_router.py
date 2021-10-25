import pytest


def test_auth_sign_up(app):
    with app.test_client() as test_client:
        response = test_client.post('api/v1/auth/signin', json={"email": "info@fithm.com", "password": "Horse@20180902"})
        assert response.status_code == 200
