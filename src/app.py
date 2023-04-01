from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/get_location", methods=["POST"])
def get_location():
    input_text = request.form.get("location_input", "")
    return "You entered: " + input_text
