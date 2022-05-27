def test_business_collection_post(app):
    with app.test_client() as test_client:
        response = test_client.post('/api/v1/business', json={"business_id": 2, "create_business": True})
        assert response.status_code == 200


def test_business_get(app, business):
    with app.test_client() as test_client:
        response = test_client.get(f'/api/v1/business/{business.id}', query_string={"business_id": business.id})
        assert response.status_code == 200