import os
from threading import Lock
from urllib import parse

from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template

from components.hike.hike_application import hikes
from components.forecast.forecast_data_gateway import db
from components.forecast.forecast_record import Forecast
from components.metrics.metrics_controller import metrics

APP_NAME = "WSIHT"

index = Blueprint("index", APP_NAME, template_folder="src/templates")
health = Blueprint("health", APP_NAME)


@index.route("/")
def index_blueprint():
    return render_template("index.html")


@health.route("/health")
def health_blueprint():
    return ("OK", 200)


def create_app():
    app = Flask(APP_NAME)

    # register /metrics route
    metrics.init_app(app)

    db_url = parse.urlsplit(os.getenv("DATABASE_URL", ""))
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + db_url.netloc + db_url.path

    db.init_app(app)
    with app.app_context(), Lock():
        db.create_all()

    app.register_blueprint(index)
    app.register_blueprint(hikes)
    app.register_blueprint(health)
    return app


if __name__ == "__main__":
    load_dotenv()
    app = create_app()
