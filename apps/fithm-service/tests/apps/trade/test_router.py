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


def test_trade_get(app, business, trade_with_portfolios_accounts):
    with app.test_client() as test_client:
        response = test_client.get(
            f"/api/v1/trades/{trade_with_portfolios_accounts.id}",
            query_string={"business_id": business.id},
        )
        assert response.status_code == 200


def test_trade_put(app, business, trade_with_portfolios_accounts):
    with app.test_client() as test_client:
        response = test_client.put(
            f"/api/v1/trades/{trade_with_portfolios_accounts.id}",
            json={"business_id": business.id},
        )
        assert response.status_code == 200


def test_trade_put_add_portfolio(app, business, trade_with_portfolios_accounts, portfolio):
    with app.test_client() as test_client:
        response = test_client.post(
            f"/api/v1/trades/{trade_with_portfolios_accounts.id}/portfolios", json={'business_id': business.id,
                                                           "portfolios": [portfolio.id]
                                                                                    }
        )
    assert response.status_code == 200


def test_trade_get_with_portfolio_account_account_position(app, business, trade_with_portfolios, portfolio_account_account_position):
    with app.test_client() as test_client:
        response = test_client.post(
            f"/api/v1/trades/{trade_with_portfolios.id}/portfolios", json={'business_id': business.id,
                                                           "portfolios": [portfolio_account_account_position.id]
                                                                                    }
        )
    assert response.status_code == 200


def test_trade_get_instructions(app, business, trade_with_portfolios_accounts, portfolio_account_account_position):
    with app.test_client() as test_client:
        response = test_client.get(
            f"/api/v1/trades/{trade_with_portfolios_accounts.id}/instructions", query_string={"business_id": business.id},
        )
    assert response.status_code == 200

