def test_portfolio_collection_get(app, business):
    with app.test_client() as test_client:
        response = test_client.get(f"/api/v1/portfolios", query_string={"business_id": business.id})
        assert response.status_code == 200


def test_portfolio_collection_post(app, business):
    with app.test_client() as test_client:
        response = test_client.post(f"/api/v1/portfolios", json={"business_id": business.id, "name": "test_portfolio"})
        assert response.status_code == 200