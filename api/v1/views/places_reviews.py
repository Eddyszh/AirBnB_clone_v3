#!/usr/bin/python3
"""Review Module
    Create a new view for Review object that
    handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all reviews objects of a place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = []
    all_reviews = storage.all('Review')
    for key, value in all_reviews.items():
        if value.place_id == str(place_id):
            reviews.append(value.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    reviews = storage.all('Review').values()
    review = [review.to_dict() for review in reviews if review.id == review_id]
    if review is None:
        abort(404)
    review.remove(review[0])
    for del_review in reviews:
        if del_review.id == review_id:
            storage.delete(del_review)
            storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        return jsonify({"error" : "Not a JSON"}), 400
    if "user_id" not in content:
        return jsonify({"error" : "Missing user_id"}), 400
    user = storage.get('User', content['user_id'])
    if user is None:
        abort(404)
    if "text" not in content:
        return jsonify({"error" : "Missing text"}), 400
    uid = content['user_id']
    text = content['text']
    new_review = Review(user_id=uid, text=text, place_id=place_id)
    for key, value in content.items():
        setattr(new_review, key, value)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a review object"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    content = request.get_json()
    if content is None:
        return jsonify({"error" : "Not a JSON"}), 400
    for key, value in content.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
