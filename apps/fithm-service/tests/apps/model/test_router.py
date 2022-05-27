def test_model_position_collection_put(app, model, business):
    with app.test_client() as test_client:
        response = test_client.put(f"/api/v1/models/{model.id}/position", json={"business_id": business.id, 'model_id': model.id, "positions":[]})
        assert response.status_code == 200

