from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from flasgger import Swagger
from flask_restful import Api, Resource

from model import *
from schemas import *

app = Flask(__name__)
CORS(app)
api = Api(app)

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "Crypto Portfolio API",
}

swagger = Swagger(app, config=swagger_config)

class HomeResource(Resource):
    def get(self):
        """
        Welcome to the home page!

        ---
        tags:
            - Welcome
        responses:
            200:
                description: A welcome message
        """
        return {"message": "Welcome to the home page"}


class ExecOrderResource(Resource):
    def post(self):
        """
        Welcome to the home page!

        ---
        tags:
            - Welcome
        parameters:
            - name: symbol
              in: formData
              type: string
              required: true
            - name: side
              in: formData
              type string
              required: true
            - name: quantity
              in: formData
              type: float
              required: true
            - name: price
              in: formData
              type: float
              required: true
            - name: currency
              in: formData
              type: string
              required: true
        responses:
            200:
                description: A welcome message
        """
        json_data = request.form
        json_data = exec_order_schema.dump(json_data)

        try:
            session = Session()

            find_portfolio = session.query(Portfolio).filter(Portfolio.symbol == json_data["symbol"]).first()

            if not find_portfolio:
                # Create a new portfolio entry if it doesn't exist
                new_portfolio = {"symbol": json_data["symbol"], "quantity": 0, "price": 0}
                find_portfolio = Portfolio(**new_portfolio)
                session.add(find_portfolio)

            if json_data["side"] == "BUY":
                find_portfolio.quantity += json_data["quantity"]
                find_portfolio.price += json_data["price"]
            elif json_data["side"] == "SELL":
                find_portfolio.quantity -= json_data["quantity"]
                find_portfolio.price -= json_data["price"]
            else:
                return jsonify({"error": "Invalid side specified"}), 400

            new_order = ExecOrder(**json_data)
            session.add(new_order)
            session.commit()

            return jsonify(json_data)

        except Exception as e:
            # Handle exceptions, such as database errors
            session.rollback()
            return jsonify({"error": str(e)}), 500

api.add_resource(HomeResource, "/")
api.add_resource(ExecOrderResource, "/exec_order")
