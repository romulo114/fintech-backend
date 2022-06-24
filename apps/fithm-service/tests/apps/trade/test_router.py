def test_trade_collection_get(app, business):
    with app.test_client() as test_client:
        response = test_client.get(
            f"/api/v1/trades", query_string={"business_id": business.id}
        )
        assert response.status_code == 200


def test_trade_collection_post(app, business):
    with app.test_client() as test_client:
        response = test_client.post(
            f"/api/v1/trades",
            json={"business_id": business.id, "name": "test_trade"},
        )
        assert response.status_code == 200


def test_trade_get(app, business, trade):
    with app.test_client() as test_client:
        response = test_client.get(
            f"/api/v1/trades/{trade.id}",
            query_string={"business_id": business.id},
        )
        assert response.status_code == 200


def test_trade_put(app, business, trade):
    with app.test_client() as test_client:
        response = test_client.put(
            f"/api/v1/trades/{trade.id}",
            json={"business_id": business.id},
        )
        assert response.status_code == 200


def test_trade_put_add_portfolio(app, business, trade, portfolio):
    with app.test_client() as test_client:
        response = test_client.post(
            f"/api/v1/trades/{trade.id}/portfolios", json={'business_id': business.id, "portfolios": [portfolio.id]
                                                           }
        )
    assert response.status_code == 200