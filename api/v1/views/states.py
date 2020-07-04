#!/usr/bin/python3
"""states"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states',methods=['GET'])
def get_states():
    """Get info about all states """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Get info about specific state """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Delete state"""
    state = storage.get("State", id=state_id)
    if state is None:
        abore(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=['POST'])
def create_state():                                                                                                         """Creat new state """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = models.state.State(name=request.json['name'])
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """ update state"""
    if not request.json:
        abort(400, "Not a JSON")
    state = storage.get("State", id=state_id)
    if state:
        state.name = request.json['name']
        state.save()
        return jsonify(state.to_dict()), 200
    abort(404)
