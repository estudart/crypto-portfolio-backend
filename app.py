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
    
api.add_resource(HomeResource, "/")
