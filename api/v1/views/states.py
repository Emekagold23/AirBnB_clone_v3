#!/usr/bin/python3
"""Contains the states view for the API"""


from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """retrieves all states"""
    all_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state_by_id(state_id=None):
    """get state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
            strict_slashes=False)
def delete_state(state_id=None):
    """deletes state by Id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """creates State object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing Name"}), 400)
    json_data = request.get_json()
    state = State(**json_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                    strict_slashes=False)
def update_state(state_id=None):
    """updates a state"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    json_data = request.get_json()
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
