#!/usr/bin/python3
"""Reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """get info about all reviews for a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    """get review info for specified review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    all_places = request.get_json()
    if 'user_id' not in all_places:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", all_places['user_id'])
    if user is None:
        abort(404)
    if 'text' not in all_places:
        return jsonify({'error': 'Missing text'}), 400
    all_places['place_id'] = place_id
    review = Review(**all_places)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    """update a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)
    storage.save()
    return jsonify(review.to_dict()), 200
