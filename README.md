# Python Flask Crypto API

![API_BackEnd](https://github.com/estudart/Crypto_Portfolio_Managment/blob/main/images/API_Doc.PNG)

## Description
This repository contains a Flask project for building a RESTful API to manage information about a Crypto Portfolio WebApp. Here I have created all the back-end that manages user interactiion with the website such as login, register, post new orders and also getting information about executed orders and portfolio.

## Technologies Used
- **Backend**: Flask, SQLAlchemy, Marshmallow, JWT
- **Database**: SQLite
- **Documentation**: Swagger

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/estudart/Crypto_Portfolio_Managment.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the Flask application:
   ```bash
   python app.py
2. Access the API documentation at http://127.0.0.1:5000/apidocs/ to explore available endpoints and interact with the API.


## Endpoints


![API_BackEnd](https://github.com/estudart/Crypto_Portfolio_Managment/blob/main/images/BackEnd_Code.PNG)

- "/portfolio":
  - "GET": Retrieve portfolio information
  - "POST": Create a new portfolio
- "/portfolio/<symbol>":
  - "DELETE": Delete portfolio information
- "/exec_order":
  - "POST": Post a new order
  - "GET": Get executed orders
- "/register_user":
  - "POST": Register a new user on the application
- "/login":
  - "POST": Login of user into the application

