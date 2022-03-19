import pytest


def test_model_list(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/v1/accounts', data={"user_id": 1})

        assert response.status_code == 200