import pytest


def test_create_business(app):
    with app.test_client() as test_client:
        response = test_client.post('/api/v1/business', json={"business_id": 2, "create_business": True})
        assert response.status_code == 200


def test_account_list(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/v1/accounts', query_string={"business_id": 1})

        assert response.status_code == 200

def test_create_account(app):
    with app.test_client() as test_client:
        response = test_client.post("/api/v1/accounts", json={'broker_name': 'test_broker', 'account_number': 'test_number', 'business_id': 1})
        assert response.status_code == 200
