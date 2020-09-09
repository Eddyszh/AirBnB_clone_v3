#!/usr/bin/python3
"""App Module
    Return the status of the API
"""
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from api.v1.views.index import *

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def errorhandler(error):
    """Returns a json formatted 404 status code"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
