#!/usr/bin/python3
"""view for State objects that handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_amenities():
    """retrieves all amenities"""
    all = storage.all(Amenity).values()
    listAmenities = []
    for x in all:
        listAmenities.append(x.to_dict())
    return jsonify(x)


@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenity(amenity_id):
    """retrieves one amenity"""
    x = storage.get(Amenity, amenity_id)
    if not x:
        abort(404)
    return jsonify(x.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity"""
    x = storage.get(Amenity, amenity_id)
    if not x:
        abort(404)
    storage.delete(x)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    amenityInfo = request.get_json()
    data = Amenity(**amenityInfo)
    data.save()
    return make_response(jsonify(data.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignoredKeys = ['id', 'created_at', 'updated_at']
    x = storage.get(Amenity, amenity_id)
    if not x:
        abort(404)
    amenityInfo = request.get_json
    for key, value in amenityInfo.items():
        if key not in ignore:
            setattr(x, key, value)
    storage.save()
    return make_response(jsonify(x.to_dict()), 200)
