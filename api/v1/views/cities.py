#!/usr/bin/python3
"""Cities Module
    Retrieves the list of city objects in state
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_citites(state_id):
    """Retrieves a list of city objects"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    all_cities = storage.all("City")
    for key, value in all_cities.items():
        if value.state_id == str(state_id):
            cities.append(value.to_dict())
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    cities = storage.all("City").values()
    city = [city.to_dict() for city in cities if city.id == city_id]
    if city is None:
        abort(404)
    city.remove(city[0])
    for del_city in cities:
        if del_city.id == city_id:
            storage.delete(del_city)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a city object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify({"error" : "Not a JSON"}), 400
    if "name" not in content:
        return jsonify({"error" : "Missing name"}), 400
    content['state_id'] = state.id
    city = City(**content)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a city object"""
    ignore = ["id", "created_at", "updated_at", "state_id"]
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify({"error" : "Not a JSON"}), 400
    for key, value in content.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
