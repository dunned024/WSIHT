from flask import Blueprint, request

from components.geography.coordinates import get_coord_box
from components.geography.location import get_location
from components.trail.trails import get_trails

hikes = Blueprint('hikes_blueprint', __name__, template_folder='src/templates')


@hikes.route("/hikes", methods=["POST"])
def hikes_blueprint():
    input_text = request.form.get("location_input", "")
    location = get_location(input_text)
    if location is None:
        return "Invalid location. Try entering a City or ZIP Code."
    coord_box = get_coord_box(location)
    trails = get_trails(coord_box)
    return trails
    # return render_template("trails.html", trails=trails)
    # return "You entered: " + str(location)
