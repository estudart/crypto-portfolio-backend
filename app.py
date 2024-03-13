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

class RegisterUser(Resource):
    def post(self):
        """
        Register a new user on the application

        ---
        tags:
            - Register
            
        parameters:
            - name: email
              in: formData
              type: string
              required: true
            - name: password
              in: formData
              type: string
              required: true
        """
        if request.form:
            data = request.form
        elif request.json:
            data = request.json

        session = Session()

        # Checks if the user is already registered on the database
        if session.query(Users).filter(Users.email == data['email']).first():
            return {"message": "user already registered"}
        
        # Adds a new user to the database
        user = Users(
            email=data['email'],
            # Encrypts the user´s password 
            password=pbkdf2_sha256.hash(data['password'])
        )

        session.add(user)
        session.commit()

        return {"message": "User created"}


class UserLogin(Resource):
    def post(self):
        """
        Login of user into the application

        ---
        tags:
            - Login
            
        parameters:
            - name: email
              in: formData
              type: string
              required: true
            - name: password
              in: formData
              type: string
              required: true
        """

        if request.form:
            data = request.form
        elif request.json:
            data = request.json
        data = request.json
        print(data['email'])

        session = Session()

        # getting the user in the data base
        user = session.query(Users).filter(Users.email == data['email']).first()

        # Checking if the user password matches with the encrypted password
        if user and pbkdf2_sha256.verify(data['password'], user.password):

            # Setting a expire time for the jwt token
            expires = timedelta(hours=24)

            # Creating the access_token, sending on it the user.id
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return {"access_token": access_token}

        # if the user does not exist, return invalid credentials
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
        Delete portfolio information

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
        Post a new order

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
              type: string
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
        """
        if request.form:
            data = request.form
        elif request.json:
            data = request.json
        print(data['symbol'])
        print(data['quantity'])
        print(data['currency'])
        current_user_id = get_jwt_identity()
        print(current_user_id)

        try:
            session = Session()

            # Check if the portfolio exists for the symbol and user ID
            find_portfolio = session.query(Portfolio).filter(Portfolio.symbol == data["symbol"], Portfolio.user_id == current_user_id).first()

            if not find_portfolio:
                # Create a new portfolio entry if it doesn't exist
                new_portfolio = {"symbol": data["symbol"], "quantity": 0, "price": 0, "user_id": current_user_id}
                find_portfolio = Portfolio(**new_portfolio)
                session.add(find_portfolio)

            # Update portfolio based on order
            if data["side"] == "BUY":
                find_portfolio.quantity += data["quantity"]
                find_portfolio.price += data["price"]
            elif data["side"] == "SELL":
                find_portfolio.quantity -= data["quantity"]
                find_portfolio.price -= data["price"]
            else:
                return {"error": "Invalid side specified"}, 400

            # Create a new order entry
            user_order = {"symbol": data["symbol"], "side": data["side"], "quantity": data["quantity"], "price": data["price"], "currency": data["currency"],"user_id": current_user_id}
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

api.add_resource(PortfoliosResource, "/portfolio")
api.add_resource(PortfolioResource, "/portfolio/<string:symbol>")
api.add_resource(ExecOrderResource, "/exec_order")
api.add_resource(RegisterUser, "/register_user")
api.add_resource(UserLogin, "/login")
