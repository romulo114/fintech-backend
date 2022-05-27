def test_account_collection_get(app, business):
    with app.test_client() as test_client:
        response = test_client.get('/api/v1/accounts', query_string={"business_id": business.id})
        assert response.status_code == 200


def test_account_collection_post(app, business):
    with app.test_client() as test_client:
        response = test_client.post("/api/v1/accounts", json={'broker_name': 'test_broker', 'account_number': 'test_number', 'business_id': business.id})
        assert response.status_code == 200


def test_account_put(app, business, account):
    with app.test_client() as test_client:
        response = test_client.put(f"/api/v1/accounts/{account.id}", json={'broker_name': 'test_change', 'account_number': 'test_number', 'business_id': business.id})
        assert response.status_code == 200


def test_account_delete(app, business, account):
    with app.test_client() as test_client:
        response = test_client.delete(f"/api/v1/accounts/{account.id}", query_string={"business_id": business.id})
        assert response.status_code == 200