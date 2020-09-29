#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
import uuid
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/4-hbnb/', strict_slashes=False)
def filters():
    """Display a HTML page"""
    classes = {'State': State, 'Amenity': Amenity, 'Place': Place}
    states = storage.all(classes["State"]).values()
    amenities = storage.all(classes['Amenity']).values()
    places = storage.all(classes['Place']).values()
    cache_id = uuid.uuid4()
    return render_template('3-hbnb.html', states=states,
                           amenities=amenities, places=places,
                           cache_id=cache_id)


@app.teardown_appcontext
def teardown_db(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
