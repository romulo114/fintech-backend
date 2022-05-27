def test_business_collection_post(app):
    with app.test_client() as test_client:
        response = test_client.post('/api/v1/business', json={"business_id": 2, "create_business": True})
        assert response.status_code == 200
