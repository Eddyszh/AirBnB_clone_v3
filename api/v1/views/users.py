#!/usr/bin/python3
"""User Module
    Create a new view for User object that
    handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retieves the list of all users"""
    users = []
    all_users = storage.all("User").values()
    for user in all_users:
        users.append(user.to_dict())
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes an user object"""
    users = storage.all('User').values()
    user = [user.to_dict() for user in users if user.id == user_id]
    if user is None:
        abort(404)
    user.remove(user[0])
    for del_user in users:
        if del_user.id == user_id:
            storage.delete(del_user)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an user object"""
    content = request.get_json()
    if content is None:
        return jsonify({"error" : "Not a JSON"}), 400
    if "email" not in content:
        return jsonify({"error" : "Missing email"}), 400
    if "password" not in content:
        return jsonify({"erro" : "Missing password"}), 400
    user_email = content['email']
    user_password = content['password']
    new_user = User(email=user_email, password=user_password)
    for key, value in content.items():
        setattr(new_user, key, value)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates an user object"""
    ignore = ["id", "email", "created_at", "updated_at"]
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    content = request.get_json()
    if content is None:
        return jsonify({"error" : "Not a JSON"}), 400
    for key, value in content.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
