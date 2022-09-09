#!/usr/bin/python3
"""view for City objects that handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrive_cities(state_id):
    """retrieves list of all cities of a state"""
    cityList = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def retrieve_cities(city_id):
    """retrieves specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes city"""
    x = storage.get(City, city_id)
    if not x:
        abort(404)
    storage.delete(x)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', 
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates city"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cityInfo = request.get_json()
    data = City(**cityInfo)
    data.state_id = state.id
    data.save()
    return make_response(jsonify(data.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates city"""
    if not request.json:
        abort(400, description="Not a JSON")
    ignoredKeys = ['id', 'state_id', 'created_at', 'updated_at']
    x = storage.get(City, city_id)
    if not x:
        abort(404)
    cityInfo = request.json
    for key, value in cityInfo.items():
        if key not in ignoredKeys:
            setattr(x, key, value)
    storage.save()
    return make_response(jsonify(x.to_dict()), 200)
