#!/usr/bin/python3
"""view for User objects that handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_users():
    """retrieves all users"""
    all = storage.all(User).values()
    userList = []
    for x in all:
        userList.append(x.to_dict())
    return jsonify(userList)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """retrieves only one user"""
    x = storage.get(User, user_id)
    if not x:
        abort(404)
    return jsonify(x.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes user"""
    x = storage.get(User, user_id)
    if not x:
        abort(404)
    storage.delete(x)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    userInfo = request.get_json()
    data = User(**userInfo)
    data.save()
    return make_response(jsonify(data.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates user"""
    x = storage.get(User, user_id)
    if not x:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignoredKeys = ['id', 'email', 'created_at', 'updated_at']
    userInfo = request.get_json()
    for key, value in userInfo.items():
        if key not in ignoredKeys:
            setattr(x, key, value)
    storage.save()
    return make_response(jsonify(x.to_dict()), 200)
