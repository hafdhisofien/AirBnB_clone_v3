#!/usr/bin/python3
""" API flask app """

from models import storage
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_request(self):
    """ Method to close session """
    storage.close()




host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or '5000'

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
