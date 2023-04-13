import os

from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template

from components.hike.hike_application import hikes
from components.forecast.forecast_data_gateway import db
from components.forecast.forecast_record import Forecast


APP_NAME = "WSIHT"

index = Blueprint('index', APP_NAME, template_folder='src/templates')


@index.route('/')
def index_blueprint():
    return render_template('index.html')


def create_app():
    app = Flask(APP_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(index)
    app.register_blueprint(hikes)
    return app


if __name__ == "__main__":
    load_dotenv()
    app = create_app()
