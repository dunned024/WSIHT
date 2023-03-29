from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")
    return """
     <form action="/get_location" method="POST">
         <input name="location_input">
         <input type="submit" value="Enter location">
     </form>
     """


@app.route("/scripts")
def scripts():
    return """
    <script>
        $SCRIPT_ROOT = {{ request.script_root|tojson }};
    </script>
    <script src="{{ url_for('static', filename='jquery.js') }}"></script>
    <script src="http://maps.googleapis.com/maps/api/js?libraries=places"></script>
    <script src="jquery.geocomplete.js"></script>
    """


@app.route("/homepage/")
def interactive():
    template = url_for("static", filename="homepage.html")
    return render_template(template)


@app.route("/get_location", methods=["POST"])
def get_location():
    input_text = request.form.get("location_input", "")
    return "You entered: " + input_text
