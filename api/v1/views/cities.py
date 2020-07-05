#!/usr/bin/python3
"""City"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.state import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Get info about all cities"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """Get info about specific city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete(city)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/<states_id>/cities', methods=['POST'])
def create_city(states_id):
    """Create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    city = models.city.City(name=request.json['name'], state_id=states_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    city.name = request.json['name']
    city.save()
    return jsonify(city.to_dict()), 200
