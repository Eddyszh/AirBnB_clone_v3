#!/usr/bin/python3
"""App Module
    Return the status of the API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def errorhandler(error):
    """Returns a json formatted 404 status code"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    """Remove the current session"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', default="0.0.0.0")
    port = int(os.getenv('HBNB_API_PORT', default=5000))
    app.run(host=host, port=port, threaded=True)
