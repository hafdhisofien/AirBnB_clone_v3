#!/usr/bin/python3
"""Places"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'])
def get_places(city_id):
    """get info about all places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'])
def get_place(place_id):
    """get info of a specific place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    all_places = request.get_json()
    if 'user_id' not in all_places:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", all_places['user_id'])
    if user is None:
        abort(404)
    if 'name' not in all_places:
        return jsonify({'error': 'Missing name'}), 400
    kwargs['city_id'] = city_id
    place = Place(**all_places)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'])
def update_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searcj for a place"""
    if request.get_json() is not None:
        search = request.get_json()
        states = search.get('states', [])
        cities = search.get('cities', [])
        amenities = search.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        places_a = []
        for place in places:
            place_amenities = place.amenities
            places_a.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    places_a.pop()
                    break
        return jsonify(places_a)
    else:
        return jsonify({'error': 'Not a JSON'}), 400
