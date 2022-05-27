def test_model_collection_get(app, business):
    with app.test_client() as test_client:
        response = test_client.get(f"/api/v1/models", query_string={"business_id": business.id})
        assert response.status_code == 200


def test_model_collection_post(app, business):
    with app.test_client() as test_client:
        response = test_client.post(f"/api/v1/models", json={"business_id": business.id, "name": "test_model"})
        assert response.status_code == 200


def test_model_get(app, business, model):
    with app.test_client() as test_client:
        response = test_client.get(f"/api/v1/models/{model.id}", query_string={"business_id": business.id})
        assert response.status_code == 200


def test_model_put(app, business, model):
    with app.test_client() as test_client:
        response = test_client.put(f"/api/v1/models/{model.id}", json={"business_id": business.id, "name": "test_change"})
        assert response.status_code == 200


def test_model_position_collection_put(app, model, business):
    with app.test_client() as test_client:
        response = test_client.put(f"/api/v1/models/{model.id}/position", json={"business_id": business.id, 'model_id': model.id, "positions":[]})
        assert response.status_code == 200

