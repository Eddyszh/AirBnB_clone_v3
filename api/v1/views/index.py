#!/usr/bin/python3
"""Index Module
    Returns a json with status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})
