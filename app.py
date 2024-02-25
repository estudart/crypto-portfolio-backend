from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from flasgger import Swagger
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256


from model import *
from schemas import *

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "12521164106679473705742150032613387626"

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


class RegisterUser(Resource):
    def post(self):

        session = Session()

        if session.query(Users)

        return


class PortfoliosResource(Resource):
    def get(self):
        """
        Get portfolio information

        ---
        tags:
            - Portfolio
        responses:
            200:
                description: A welcome message
        """
        session = Session()
        portfolio_all = session.query(Portfolio).all()
        portfolio_json = portfolios_schema.dump(portfolio_all)
        return portfolio_json

class PortfolioResource(Resource):   
    def delete(self, symbol):
        """
        Get portfolio information

        ---
        tags:
            - Portfolio
        parameters:
            - name: symbol
              in: path
              type: string
              required: true
        responses:
            200:
                description: A welcome message
        """
        session = Session()
        found_crypto = session.query(Portfolio).filter(Portfolio.symbol == symbol)
        found_crypto.delete()
        session.commit()
        return {"message": "Success"}



class ExecOrderResource(Resource):
    def post(self):
        """
        Get information regarding the executed orders

        ---
        tags:
            - Executed Orders
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
        json_data = request.json
        json_data = exec_order_schema.dump(json_data)
        print(request.json['symbol'])


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

            return {"message": "Success"}

        except Exception as e:
            # Handle exceptions, such as database errors
            session.rollback()
            return {"error": str(e)}, 500
    
    def get(self):
        """
        Get executed orders

        ---
        tags:
            - Executed Orders
        responses:
            200:
                description: A welcome message
        """
        session = Session()
        exec_orders = session.query(ExecOrder).all()
        json_exec_orders = exec_orders_schema.dump(exec_orders)
        return json_exec_orders

api.add_resource(HomeResource, "/")
api.add_resource(PortfoliosResource, "/portfolio")
api.add_resource(PortfolioResource, "/portfolio/<string:symbol>")
api.add_resource(ExecOrderResource, "/exec_order")
