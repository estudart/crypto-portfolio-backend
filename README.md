# Python Flask Planets API

![API_BackEnd](https://github.com/estudart/planets-api/blob/main/API_BackEnd.PNG)

## Description
This repository contains a Flask project for building a RESTful API to manage information about a Crypto Portfolio WebApp. Here I have created all the back that manages user interactiion
with the website such as login, register, post new orders and also getting information about executed orders and portfolio.

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

[API Documentation](https://estudart.pythonanywhere.com/apidocs/)

![API_BackEnd](https://github.com/estudart/planets-api/blob/main/Doc.PNG)

- `/planets`:
  - `GET`: Retrieve a list of planets.
  - `POST`: Create a new planet.
- `/planet/<id>`:
  - `GET`: Retrieve information about a specific planet.
  - `PUT`: Update information about a specific planet.
  - `DELETE`: Delete a specific planet.
- `/user/<id>`:
  - `GET`: Retrieve information about a specific user.
  - `PUT`: Update information about a specific user.
  - `DELETE`: Delete a specific user.
- `/users`:
  - `GET`: Retrieve a list of all users.
  - `POST`: Create a new user.
- `/create_planets`:
  - `GET`: Populate the database with predefined planet data.
