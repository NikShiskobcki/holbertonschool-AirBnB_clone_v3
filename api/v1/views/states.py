#!/usr/bin/python3
"""view for State objects that handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_states(state_id=None):
	"""retrieves list of all states or only one"""
	if state_id == None:
		all = storage.all(State).values()
		listStates = []
		for x in all:
			listStates.append(x.to_dict())
		return jsonify(listStates)
	else:
		x = storage.get(State, state_id)
		if not x:
			abort(404)
		return jsonify(x.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)	
def delete_state(state_id):
	"""deletes state"""
	x = storage.get(State, state_id)
	if not x:
		abort(404)
	storage.delete(x)
	storage.save()
	return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
	"""creates state"""
	if not request.json:
		abort(400, description="Not a JSON")
	if 'name' not in request.json:
		abort(400, description="Missing name")
	stateInfo = request.json
	data = State(**stateInfo)
	data.save()
	return make_response(jsonify(data.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
	"""updates state"""
	if not request.json:
		abort(400, description="Not a JSON")
	ignoredKeys = ['id', 'created_at', 'updated_at']
	x = storage.get(State, state_id)
	if not x:
		abort(404)
	stateInfo = request.json
	for key, value in stateInfo.items():
		if key not in ignoredKeys:
			setattr(state, key, value)
	storage.save()
	return make_response(jsonify(x.to_dict()), 200)
