from typing import Optional, Union

from libs.database.business import remove_free_business_prices
from apps.model.models import ModelPositionPrice, ModelPosition
from apps.business.models import BusinessPrice
from flask import current_app, g, abort
from libs.database import db_session
from apps.models import Model, Business

# from libs.database import helpers


class ModelView:
    def __init__(self):
        pass

    def get_models(self, args: dict) -> list:
        """Get all models for the business"""

        business: Business = g.business
        public = args.get("public", "false") == "true"
        current_app.logger.debug(
            f"public arg was {args.get('public', 'not set so it is false')}"
        )
        models: list[Model] = (
            self.public_models()
            if public
            else filter(lambda model: not model.is_public, business.models)
        )
        return {"models": [model.as_dict() for model in models if model.active]}

    def create_model(self, body: dict) -> dict:
        """Create a new model for the business"""

        public = body.get("public", False)
        model = Model(
            business_id=g.business.id,
            name=body["name"],
            description=body.get("description"),
            keywords=body.get("keywords"),
            is_public=public,
        )
        db_session.add(model)
        db_session.commit()

        return model.as_dict()

    def get_model(self, id: int) -> dict:
        """Get a specific model with id"""

        model = self.__get_model(id)
        if not model.active:
            abort(401, "Not active model")

        return model.as_dict(True)

    def update_model(self, id: int, body: dict) -> dict:
        """Update a model with body"""

        model = self.__get_model(id)
        model.name = body.get("name", model.name)
        model.keywords = body.get("keywords", model.keywords)
        model.is_public = body.get("public", model.is_public)
        model.description = body.get("description", model.description)

        db_session.commit()

        return model.as_dict()

    def delete_model(self, id: int):
        """Delete a model"""

        model = self.__get_model(id)
        for position in model.allocation:
            if position.model_position_price:
                db_session.delete(position.model_position_price)
        db_session.delete(model)
        db_session.commit()
        # helpers.update_trades_for_pendings(pendings)

        return {"result": "success"}

    def update_model_position(self, id: int, body: dict) -> dict:
        """Update positions for the model"""

        if 'positions' not in body:
            abort(400, "Bad request")
 
        current_app.logger.info(f'Update model positions: {body["positions"]}')
        business_id = g.business.id

        model = self.__get_model(id)
        positions: list[dict] = body['positions']
        current_positions: list[ModelPosition] = model.allocation
        business_prices = self.__get_business_prices(business_id)

        for pos in positions:
            new_price = pos["price"] if "price" in pos else None
            if "id" not in pos: # new position
                new_position = ModelPosition(
                    model_id=id,
                    symbol=pos["symbol"],
                    weight=pos["weight"]
                )

                price = self.__find_or_create_price(
                    business_id,
                    business_prices,
                    new_position.symbol,
                    new_price
                )

                if price:
                    model_position_price = ModelPositionPrice(
                        model_position=new_position,
                        model_price=price,
                    )

                    db_session.add(model_position_price)

                db_session.add(new_position)
            else: # old position
                old_position = self.__find_model_position(current_positions, pos["id"])
                if "weight" in pos:
                    old_position.weight = pos["weight"]

                old_position_price: ModelPositionPrice = old_position.model_position_price
                old_position.symbol = pos["symbol"]
                price = self.__find_or_create_price(
                    business_id,
                    business_prices,
                    old_position.symbol,
                    new_price
                )

                if price:
                    if not old_position_price:
                        old_position_price = ModelPositionPrice(
                            model_position=old_position,
                            model_price=price,
                        )
                        db_session.add(old_position_price)

                    old_position_price.model_price = price
                else:
                    if old_position_price:
                        db_session.delete(old_position_price)

        # remove positions
        keep_position_ids = [pos["id"] for pos in positions if "id" in pos]
        for pos in current_positions:
            if pos.id in keep_position_ids:
                continue

            if pos.model_position_price:
                db_session.delete(pos.model_position_price)
            db_session.delete(pos)

        db_session.commit()

        # remove free business prices
        remove_free_business_prices(business_id)

        return model.as_dict(True)


    def public_models(self) -> list[Model]:

        return db_session.query(Model).filter(Model.is_public == True).all()

    def __get_model(self, id: int) -> Model:

        model = db_session.query(Model).get(id)
        if not model:
            abort(404, "Model not found")
        if model.business_id != g.business.id:
            abort(403, "You don't have permission to this model.")

        return model


    def __find_model_position(self, positions: list[ModelPosition], position_id: int) -> Optional[ModelPosition]:
        for position in positions:
            if position.id == position_id:
                return position

        return None


    def __get_business_prices(self, business_id: int) -> list[BusinessPrice]:
        return db_session.query(BusinessPrice).filter(
            BusinessPrice.business_id == business_id
        ).all()


    def __find_business_price(self, prices: list[BusinessPrice], symbol: str) -> Optional[BusinessPrice]:
        for price in prices:
            if price.symbol == symbol:
                return price

        return None


    def __find_or_create_price(
        self,
        business_id: int,
        prices: list[BusinessPrice],
        symbol: str,
        new_price: Optional[float]
    ) -> BusinessPrice:

        price = self.__find_business_price(prices, symbol)

        if not price:
            if not new_price:
                return None

            price = BusinessPrice(
                business_id=business_id,
                symbol=symbol,
                price=new_price
            )
            db_session.add(price)
        elif new_price:
            price.price = new_price

        return price