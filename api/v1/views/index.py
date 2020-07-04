#!/usr/bin/python3
""" Index of the api """

from api.v1.views import app_views
from flask import jsonify
from models import storage



@app_views.route('/status')
def status():
    """ returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
