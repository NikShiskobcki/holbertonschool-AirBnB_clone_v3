#!/usr/bin/python3
"""view for place-amenity objects that handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenities_in_place(place_id):
    """retrieves all ameni in place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_in_place(place_id, amenity_id):
    """deletes review"""
    x = storage.get(Amenity, amenity_id)
    if not x:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    if x not in amenities:
        return make_response(jsonify(x.to_dict()), 200)
    storage.delete(x)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """link amenity w/ place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    if amenity in amenities:
        return jsonify(amenity.to_dict())
