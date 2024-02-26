from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from flasgger import Swagger
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta

from model import *
from schemas import *

app = Flask(__name__)
CORS(app)
api = Api(app)


app.config["JWT_SECRET_KEY"] = "12521164106679473705742150032613387626"
jwt = JWTManager(app)

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

        json_data = request.json
        #json_data = user_schema.dump(json_data)

        session = Session()

        if session.query(Users).filter(Users.email == json_data['email']).first():
            return {"message": "user already registered"}
        
        user = Users(
            email=json_data['email'], 
            password=pbkdf2_sha256.hash(json_data['password'])
        )

        session.add(user)
        session.commit()

        return {"message": "User created"}, 201


class UserLogin(Resource):
    def post(self):
        json_data = request.json
        print(json_data['email'])

        session = Session()

        user = session.query(Users).filter(Users.email == json_data['email']).first()

        if user and pbkdf2_sha256.verify(json_data['password'], user.password):
            expires = timedelta(hours=24)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return {"access_token": access_token}

        return {"message": "Invalid credentials"}

class PortfoliosResource(Resource):
    @jwt_required()
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
        current_user_id = get_jwt_identity()
        session = Session()
        portfolio_all = session.query(Portfolio).filter(Portfolio.user_id == current_user_id).all()
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
    @jwt_required()
    def post(self):
        """
        Get information regarding the executed orders

        """
        json_data = request.json
        print(json_data['symbol'])
        current_user_id = get_jwt_identity()
        print(current_user_id)

        try:
            session = Session()

            # Check if the portfolio exists for the symbol and user ID
            find_portfolio = session.query(Portfolio).filter(Portfolio.symbol == json_data["symbol"], Portfolio.user_id == current_user_id).first()

            if not find_portfolio:
                # Create a new portfolio entry if it doesn't exist
                new_portfolio = {"symbol": json_data["symbol"], "quantity": 0, "price": 0, "user_id": current_user_id}
                find_portfolio = Portfolio(**new_portfolio)
                session.add(find_portfolio)

            # Update portfolio based on order
            if json_data["side"] == "BUY":
                find_portfolio.quantity += json_data["quantity"]
                find_portfolio.price += json_data["price"]
            elif json_data["side"] == "SELL":
                find_portfolio.quantity -= json_data["quantity"]
                find_portfolio.price -= json_data["price"]
            else:
                return {"error": "Invalid side specified"}, 400

            # Create a new order entry
            user_order = {"symbol": json_data["symbol"], "side": json_data["side"], "quantity": json_data["quantity"], "price": json_data["price"], "currency": json_data["currency"],"user_id": current_user_id}
            new_order = ExecOrder(**user_order)
            session.add(new_order)
            session.commit()

            return {"message": "Success"}

        except Exception as e:
            # Handle exceptions, such as database errors
            session.rollback()
            print(str(e))
            return {"error": str(e)}, 500

    @jwt_required()
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
        current_user_id = get_jwt_identity()
        session = Session()
        exec_orders = session.query(ExecOrder).filter(ExecOrder.user_id == current_user_id).all()
        json_exec_orders = exec_orders_schema.dump(exec_orders)
        return json_exec_orders

api.add_resource(HomeResource, "/")
api.add_resource(PortfoliosResource, "/portfolio")
api.add_resource(PortfolioResource, "/portfolio/<string:symbol>")
api.add_resource(ExecOrderResource, "/exec_order")
api.add_resource(RegisterUser, "/register_user")
api.add_resource(UserLogin, "/login")
