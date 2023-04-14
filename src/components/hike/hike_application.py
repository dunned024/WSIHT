from flask import Blueprint, request

from components.geography.coordbox_collector import get_coord_box, get_location
from components.hike.hike_analyzer import generate_hikes
from components.trail.trail_collector import get_trails

hikes = Blueprint('hikes_blueprint', __name__, template_folder='src/templates')


@hikes.route("/hikes", methods=["POST"])
def hikes_blueprint():
    input_text = request.form.get("location_input", "")
    location = get_location(input_text)
    if location is None:
        return "Invalid location. Try entering a City or ZIP Code."
    coord_box = get_coord_box(
        latitude=location.latitude,
        longitude=location.longitude,
        padding=0.1
    )
    trails = get_trails(coord_box)
    hikes = generate_hikes(trails)
    return hikes
    # return render_template("trails.html", trails=trails)
